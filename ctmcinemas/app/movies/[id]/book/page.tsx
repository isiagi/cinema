/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable prefer-const */
"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter, useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import axios from "axios"; // Make sure to import axios

interface Seat {
  id: string;
  row: string;
  number: number;
  isAvailable: boolean;
  price: number;
}

// Generate seats based on the specific arrangement and price
const generateSeats = (basePrice: number = 10.0) => {
  const rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"];
  let seats: any = [];

  rows.forEach((row, rowIndex) => {
    if (rowIndex === 0) {
      // First row: 5 pairs of seats (10 total)
      for (let pair = 0; pair < 5; pair++) {
        for (let seatInPair = 0; seatInPair < 2; seatInPair++) {
          const seatNumber = pair * 2 + seatInPair + 1;
          seats.push({
            id: `${row}${seatNumber}`,
            row,
            number: seatNumber,
            isAvailable: true, // 80% chance of being available
            price: basePrice * 1.2, // Slightly higher price for the first row
          });
        }
      }
    } else if (rowIndex < 8) {
      // Rows B-H: 3 pairs of seats + 1 single seat (7 total)
      for (let seatNumber = 1; seatNumber <= 7; seatNumber++) {
        seats.push({
          id: `${row}${seatNumber}`,
          row,
          number: seatNumber,
          isAvailable: true,
          price: basePrice,
        });
      }
    } else {
      // Rows I-J: 7 seats with a space at position 4
      for (let seatNumber = 1; seatNumber <= 7; seatNumber++) {
        seats.push({
          id: `${row}${seatNumber}`,
          row,
          number: seatNumber,
          isAvailable: true,
          price: basePrice,
        });
      }
    }
  });

  return seats;
};

export default function BookPage() {
  const searchParams = useSearchParams();
  const params = useParams();
  const router = useRouter();
  const [seats, setSeats] = useState(generateSeats());
  const [selectedSeats, setSelectedSeats] = useState<string[]>([]);

  const movieId = params.id as string;
  const date = searchParams.get("date");
  const time = searchParams.get("time");
  const editSeats = searchParams.get("seats"); // Add this to get existing seats

  const toggleSeat = (seatId: string) => {
    const seat = seats.find((s: any) => s.id === seatId);
    if (seat && seat.isAvailable) {
      setSelectedSeats((prev) =>
        prev.includes(seatId)
          ? prev.filter((id) => id !== seatId)
          : [...prev, seatId]
      );
    }
  };

  useEffect(() => {
    // Function to fetch movie showtimes
    const fetchMovieShowtimes = async () => {
      try {
        // Fetch showtimes for the specific movie
        const response = await axios.get(
          `http://127.0.0.1:8000/showings/showings/movie/${movieId}/`
        );

        console.log(response.data, "response");

        // Get the base price from the response, or use a default
        const basePrice = response.data[0].price
          ? Number.parseFloat(response.data[0].price)
          : 10.0;

        // Generate seats with the fetched price
        const generatedSeats = generateSeats(basePrice);
        setSeats(generatedSeats);
      } catch (error) {
        console.error("Error fetching showtimes:", error);

        // Fallback to default seats if fetch fails
        setSeats(generateSeats());
      }
    };

    // Call the fetch function
    fetchMovieShowtimes();

    // If editing seats, set the selected seats
    if (editSeats) {
      setSelectedSeats(editSeats.split(","));
    }
  }, [movieId, time, editSeats]);

  const handleReserve = () => {
    const selectedSeatsParam = selectedSeats.join(",");
    router.push(
      `/movies/${movieId}/eats?date=${date}&time=${time}&seats=${selectedSeatsParam}`
    );
  };

  const totalPrice = selectedSeats.reduce((total, seatId) => {
    const seat = seats.find((s: any) => s.id === seatId);
    return total + (seat?.price || 0);
  }, 0);

  // Group seats by row for easier rendering
  const seatsByRow = seats.reduce((acc: any, seat: any) => {
    if (!acc[seat.row]) {
      acc[seat.row] = [];
    }
    acc[seat.row].push(seat);
    return acc;
  }, {} as Record<string, Seat[]>);

  return (
    <div className="max-w-5xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-4">Select Your Seats</h1>
      <p className="mb-4">
        Movie: {movieId}, Date: {date}, Time: {time}
      </p>

      <div className="mb-8 overflow-x-auto">
        {/* Screen */}
        <div className="w-full h-8 bg-gray-300 rounded-t-lg mb-12 text-center text-sm leading-8">
          Screen
        </div>

        {/* Seating Area */}
        <div className="space-y-4 min-w-max">
          {Object.entries(seatsByRow).map(([row, rowSeats]: any): any => (
            <div key={row} className="flex items-center">
              {/* Row Label */}
              <div className="w-8 text-center font-bold">{row}</div>

              {/* Seats */}
              <div
                className={cn(
                  "flex",
                  row === "A" ? "justify-center" : "justify-start"
                )}
              >
                <div className="flex gap-2">
                  {rowSeats.map((seat: any, index: any) => {
                    const isEndOfPair =
                      (row === "A" &&
                        (index + 1) % 2 === 0 &&
                        index < rowSeats.length - 1) ||
                      (row !== "A" && (index + 1) % 2 === 0 && index < 6);

                    if (["I", "J"].includes(row) && seat.number === 4) {
                      return (
                        <div
                          key={seat.id}
                          className={cn("inline-flex", isEndOfPair && "mr-4")}
                        >
                          <div
                            key={seat.id}
                            className="w-8 h-8 w-8 h-8 rounded-t-lg"
                          />
                        </div>
                      ); // Empty space for seat 4
                    }

                    return (
                      <div
                        key={seat.id}
                        className={cn("inline-flex", isEndOfPair && "mr-4")}
                      >
                        <SeatButton
                          seat={seat}
                          isSelected={selectedSeats.includes(seat.id)}
                          onToggle={toggleSeat}
                        />
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex flex-col sm:flex-row justify-between items-center mb-8">
        <div>
          <p>Selected Seats: {selectedSeats.join(", ")}</p>
          <p className="font-bold">Total Price: {totalPrice.toFixed(2)} UGX</p>
        </div>
        <Button
          onClick={handleReserve}
          disabled={selectedSeats.length === 0}
          className="mt-4 sm:mt-0"
        >
          Reserve Seat{selectedSeats.length > 1 ? "s" : ""}
        </Button>
      </div>

      {/* Legend */}
      <div className="flex justify-center space-x-8">
        <div className="flex items-center">
          <div className="w-4 h-4 bg-blue-500 rounded-t-sm mr-2"></div>
          <span>Available</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-green-500 rounded-t-sm mr-2"></div>
          <span>Selected</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-gray-300 rounded-t-sm mr-2"></div>
          <span>Booked</span>
        </div>
      </div>
    </div>
  );
}

interface SeatButtonProps {
  seat: Seat;
  isSelected: boolean;
  onToggle: (seatId: string) => void;
}

function SeatButton({ seat, isSelected, onToggle }: SeatButtonProps) {
  return (
    <button
      className={cn(
        "w-8 h-8 rounded-t-lg text-sm font-bold transition-colors",
        !seat.isAvailable && "bg-gray-300 cursor-not-allowed",
        seat.isAvailable && isSelected && "bg-green-500 text-white",
        seat.isAvailable &&
          !isSelected &&
          "bg-blue-500 text-white hover:bg-blue-600"
      )}
      onClick={() => onToggle(seat.id)}
      disabled={!seat.isAvailable}
    >
      {seat.number}
    </button>
  );
}

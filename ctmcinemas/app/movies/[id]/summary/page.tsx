"use client";

import { useState, useEffect } from "react";
import { useSearchParams, useRouter, useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Edit2, Film, Calendar, Clock, Info, Utensils } from "lucide-react";
import Image from "next/image";
// import { movies } from "@/lib/movies";
import { useAuth } from "@clerk/nextjs";
import axios from "axios";
import PopupMessage from "@/components/popup";
// import { auth } from "@clerk/nextjs/server";

interface MovieDetails {
  title: string;
  image: string;
  duration: string;
  rating: string;
  screen: string;
  price: number;
  type: string;
}

interface EatsItem {
  id: string;
  name: string;
  price: number;
}

const eatsItems: EatsItem[] = [
  { id: "popcorn", name: "Popcorn", price: 5000 },
  { id: "soda", name: "Soda", price: 3000 },
  { id: "nachos", name: "Nachos", price: 7000 },
  { id: "hotdog", name: "Hot Dog", price: 6000 },
];

export default function BookingSummaryPage() {
  // const { isLoaded, isSignedIn, userId } = auth();
  const [popupMessage, setPopupMessage] = useState("");
  const [loader, setLoader] = useState(true)
  const searchParams = useSearchParams();
  const params = useParams();
  const router = useRouter();
  const [movieDetails, setMovieDetails] = useState<any>({});
  const [selectedEats, setSelectedEats] = useState<Record<string, number>>({});
  const [color, setColor] = useState<string>("");
  const [bgColor, setBgColor] = useState<string>("");

  const [user, setUser] = useState<any>({})
  const access_token = localStorage.getItem('access_token');

  const seats = searchParams.get("seats")?.split(",") || [];
  const date = searchParams.get("date");
  const time = searchParams.get("time");
  const movieId = params.id;
  const eats = searchParams.get("eats");

  const getMovieDetails = async () => {
    try {
      const date = searchParams.get("date");
      const time = searchParams.get("time");

      const showResponse = await axios.get(`http://127.0.0.1:8000/showings/showings/movie/${movieId}/`);
      const showData = showResponse.data;

      const movieResponse = await axios.get(`http://127.0.0.1:8000/movies/movies/${movieId}/`);
      const movieData = movieResponse.data;

      const filteredShow = showData.find(
        (show: any) => show.date === date && show.time === time
      );

      const showDetails = filteredShow
        ? { ...filteredShow, showId: filteredShow.id }
        : {};

      delete showDetails.id;

      const combinedDetails = {
        ...movieData,
        ...showDetails,
      };

      setLoader(false)
      setMovieDetails(combinedDetails);
    } catch (err) {
      setMovieDetails({});
      console.error("Error fetching movie/showtime details:", err);
    }
  };

  const getUserProfile = () => {
    let config = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:8000/auth/profile/',
      headers: {
        'Authorization': `Bearer ${access_token}`
      }
    };

    axios.request(config).then((response) => {
      setUser(response.data);
    }).catch((error) => {
      setUser({})
      console.log(error.response.data)
    });
  }

  // get movie details
  useEffect(() => {
    getMovieDetails()
    getUserProfile()
  }, [movieId]);

  useEffect(() => {
    if (eats) {
      const eatsObject = eats.split(",").reduce((acc, item) => {
        const [id, quantity] = item.split(":");
        acc[id] = Number.parseInt(quantity);
        return acc;
      }, {} as Record<string, number>);
      setSelectedEats(eatsObject);
    }
  }, [eats]);

  const handleEditSeats = () => {
    router.push(
      `/movies/${movieId}/book?date=${date}&time=${time}&seats=${seats.join(
        ","
      )}&editSeats=true`
    );
  };

  const handleEditEats = () => {
    router.push(
      `/movies/${movieId}/eats?date=${date}&time=${time}&seats=${seats.join(
        ","
      )}`
    );
  };

  const calculateTotal = () => {
    const seatsTotal = seats.length * movieDetails.price;
    const eatsTotal = Object.entries(selectedEats).reduce(
      (total, [itemId, quantity]) => {
        const item = eatsItems.find((i) => i.id === itemId);
        return total + (item?.price || 0) * quantity;
      },
      0
    );
    return seatsTotal + eatsTotal;
  };

  const handlePayment = async () => {
    try {
      if (!user || !user.is_active) {
        setColor("#960000");
        setBgColor("#111827");
        setPopupMessage("You need to sign in to make your payment.");
        return;
      }

      const accessToken = localStorage.getItem("access_token");
      if (!accessToken) {
        setColor("#960000");
        setBgColor("#111827");
        setPopupMessage("You are not authenticated. Please sign in again.");
        return;
      }

      const payload = {
        user: user.id,
        total_price: calculateTotal(),
        eats,
        seats,
        showing: movieDetails.showId,
      };

      await axios.post("http://127.0.0.1:8000/orders/orders/", payload, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
        withCredentials: true,
      });

      setColor("#62a03f");
      setBgColor("#111827");
      setPopupMessage("Order placed successfully!");

    } catch (error: any) {
      console.error("Error creating order:", error.response?.data || error.message);
      setColor("#960000");
      setBgColor("#111827");
      setPopupMessage("An error occurred. Please try again.");
      // alert(error.response?.data?.message || "An error occurred. Please try again.");
    }
  };

  if (loader) {
    return <div className="flex justify-center items-center h-screen w-full">Loading...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8">BOOKING SUMMARY</h1>

      {/* Movie Details Section */}
      <div className="border-b py-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Film className="h-5 w-5 text-blue-500" />
            <h2 className="text-lg font-bold">MOVIE DETAILS</h2>
          </div>
          <Button variant="ghost" size="sm" onClick={() => router.push("/")}>
            <Info className="h-4 w-4" />
          </Button>
        </div>
        <div className="flex gap-6">
          <div className="relative w-[150px] h-[200px]">
            <Image
              src={movieDetails.image || "/placeholder.svg"}
              alt={movieDetails.title}
              fill
              className="object-cover rounded-md"
            />
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-bold mb-2">{movieDetails.title}</h3>
            <p className="text-gray-600 mb-1">
              Duration: {movieDetails.duration}
            </p>
            <p className="text-gray-600 mb-1">Rating: {movieDetails.rating}</p>
            <p className="text-gray-600">Highlight: {movieDetails.highlight}</p>
          </div>
        </div>
      </div>

      {/* Show Details Section */}
      <div className="border-b py-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Calendar className="h-5 w-5 text-blue-500" />
            <h2 className="text-lg font-bold">SHOW DETAILS</h2>
          </div>
          <div className="flex items-center text-sm text-gray-600">
            <Clock className="h-4 w-4 mr-1" />
            <span>Please arrive 15 minutes before showtime</span>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-gray-600">Date: {date}</p>
            <p className="text-gray-600">Time: {time}</p>
          </div>
        </div>
      </div>

      {/* Seat Selection Section */}
      <div className="border-b py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Info className="h-5 w-5 text-blue-500" />
            <h2 className="text-lg font-bold">SEAT SELECTION</h2>
          </div>
          <Button variant="ghost" size="sm" onClick={handleEditSeats}>
            <Edit2 className="h-4 w-4" />
          </Button>
        </div>
        <div className="mt-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="font-medium">Selected Seats:</p>
            <p className="text-lg">{seats.join(", ")}</p>
            <p className="text-sm text-gray-500 mt-2">
              Standard Seating • {seats.length} seat
              {seats.length !== 1 ? "s" : ""}
            </p>
          </div>
        </div>
      </div>

      {/* Eats Selection Section */}
      <div className="border-b py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Utensils className="h-5 w-5 text-blue-500" />
            <h2 className="text-lg font-bold">EATS SELECTION</h2>
          </div>
          <Button variant="ghost" size="sm" onClick={handleEditEats}>
            <Edit2 className="h-4 w-4" />
          </Button>
        </div>
        <div className="mt-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            {Object.entries(selectedEats).map(([itemId, quantity]) => {
              const item = eatsItems.find((i) => i.id === itemId);
              if (item && quantity > 0) {
                return (
                  <div
                    key={itemId}
                    className="flex justify-between items-center mb-2"
                  >
                    <span>
                      {item.name} x {quantity}
                    </span>
                    <span>{(item.price * quantity).toLocaleString()} UGX</span>
                  </div>
                );
              }
              return null;
            })}
          </div>
        </div>
      </div>

      {/* Order Summary */}
      <div className="mt-8 bg-gray-50 p-6 rounded-lg">
        <h2 className="text-lg font-bold mb-4">ORDER SUMMARY</h2>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span>Tickets ({seats.length})</span>
            <span>
              {(seats.length * movieDetails.price).toLocaleString()} UGX
            </span>
          </div>
          <div className="flex justify-between">
            <span>{movieDetails.type}</span>
            <span>Included</span>
          </div>
          {Object.entries(selectedEats).map(([itemId, quantity]) => {
            const item = eatsItems.find((i) => i.id === itemId);
            if (item && quantity > 0) {
              return (
                <div key={itemId} className="flex justify-between">
                  <span>
                    {item.name} ({quantity})
                  </span>
                  <span>{(item.price * quantity).toLocaleString()} UGX</span>
                </div>
              );
            }
            return null;
          })}
          <div className="border-t pt-2 mt-4">
            <div className="flex justify-between font-bold">
              <span>Total Amount</span>
              <span>{calculateTotal().toLocaleString()} UGX</span>
            </div>
          </div>
        </div>
      </div>

      {/* Payment Button */}
      {popupMessage && <PopupMessage color={color} bgColor={bgColor} message={popupMessage} onClose={() => setPopupMessage("")} />}
      <div className="mt-8 flex justify-end">
        <Button size="lg" className="w-full md:w-auto" onClick={handlePayment}>
          Proceed to Payment
        </Button>
      </div>
    </div>
  );
}

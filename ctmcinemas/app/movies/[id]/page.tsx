"use client";

import { MovieDetails } from "@/types/movie";
import MovieShowtimes from "@/components/movie-showtimes";
import { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "next/navigation";

export default function MoviePage() {
  const [movieData, setMovieData] = useState<MovieDetails | null>(null);
  const {id} = useParams()

  useEffect(() => {
    const fetchMovieData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/movies/movies/");
        const movies: MovieDetails[] = response.data;

        const movie = movies.find((movie) => movie.id === id);
        if (!movie) return;

        const showtimes = ["12:00 PM", "2:30 PM", "5:00 PM", "7:30 PM", "10:00 PM"];
        const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

        const generateShowtimes = (date: Date) => {
          const dayOfWeek = daysOfWeek[date.getDay()];
          let price: number;
          let type: string;

          switch (dayOfWeek) {
            case "Monday":
              price = 8000;
              type = "3D";
              break;
            case "Tuesday":
            case "Wednesday":
              price = 12000;
              type = "3D + Popcorn";
              break;
            case "Thursday":
              price = 10000;
              type = "3D";
              break;
            default:
              price = 13000;
              type = "3D";
          }

          return showtimes.map((time) => ({
            time,
            type,
            price: price.toString(),
            dayOfWeek,
          }));
        };

        const days = Array.from({ length: 7 }, (_, i) => {
          const date = new Date();
          date.setDate(date.getDate() + i);
          return {
            date: date.toISOString().split("T")[0],
            displayDate: date.toLocaleDateString("en-US", {
              weekday: "short",
              month: "short",
              day: "numeric",
            }),
            dayOfWeek: daysOfWeek[date.getDay()],
            showtimes: generateShowtimes(date),
          };
        });

        setMovieData({ ...movie, days });
      } catch (error) {
        console.error("No movies found because of: ", error);
      }
    };

    fetchMovieData();
  }, [id]); // Fetch data when `id` changes

  if (!movieData) {
    return <p className="text-center">Loading...</p>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <MovieShowtimes movie={movieData} />
    </div>
  );
}

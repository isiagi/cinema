/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { Button } from "@/components/ui/button";
import { Calendar, Eye } from "lucide-react";
import Image from "next/image";
import React from "react";

function Page() {
  const [movies, setMovies] = React.useState([]);

  React.useEffect(() => {
    const fetchMovies = async () => {
      const response = await fetch(
        "http://127.0.0.1:8000/movies/movies/by_status/?status=NOW_SHOWING"
      );
      const data = await response.json();
      setMovies(data);
    };
    fetchMovies();
  }, []);

  const handleViewMovie = (movieId: string) => {
    window.location.href = `/movies/${movieId}`;
  };

  const handleViewShowtimes = (movieId: string) => {
    window.location.href = `/movies/${movieId}?scrollToShowtimes=true`;
  };
  return (
    <div>
      <div className="relative h-[300px] w-full">
        <Image
          src="https://media.istockphoto.com/id/1479991868/photo/theater-coming-soontext-background-3d-rendering.webp?a=1&b=1&s=612x612&w=0&k=20&c=Ui59IrxcxOQ4P6zAAJevjAOH9ukboeMg3Srk9vcEEDk="
          alt="Coming Soon Banner"
          fill
          className="object-cover"
        />
        <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
          <h1 className="text-4xl md:text-5xl font-bold text-white">
            What&apos;s On
          </h1>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 p-12">
        {movies.map((movie: any) => (
          <div key={movie.id} className="relative aspect-[2/3] group">
            <Image
              src={movie.image}
              alt={movie.title}
              fill
              className="object-cover rounded-lg"
            />
            <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg">
              <div className="absolute inset-0 flex flex-col items-center justify-center text-white p-6 text-center">
                <h2 className="text-2xl font-bold mb-2">{movie.title}</h2>
                <p className="mb-6 text-lg">{movie.description}</p>
                <div className="flex space-x-4">
                  <Button
                    variant="outline"
                    size="sm"
                    className="text-white border-white hover:bg-white hover:text-black"
                    onClick={() => handleViewMovie(movie.id)}
                  >
                    <Eye className="mr-2 h-4 w-4" />
                    View Movie
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="text-white border-white hover:bg-white hover:text-black"
                    onClick={() => handleViewShowtimes(movie.id)}
                  >
                    <Calendar className="mr-2 h-4 w-4" />
                    View Showtimes
                  </Button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Page;

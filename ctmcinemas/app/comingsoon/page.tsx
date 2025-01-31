"use client";

import { useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Clock, Star, Play, Info, X } from "lucide-react";
import dynamic from "next/dynamic";

const ReactPlayer = dynamic(() => import("react-player/lazy"), { ssr: false });

// This would typically come from an API
const upcomingMovies = [
  {
    id: "amazing-spider-man",
    title: "The Amazing Spider-Man",
    image: "/placeholder.svg?height=600&width=400&text=Spider-Man",
    rating: 9.3,
    duration: "02 hours 30 minutes",
    description:
      "Sed ut perspiciatis unde omnis iste natus error sit voluptatem...",
    language: "English",
    releaseDate: "May 19, 2022",
    genre: ["Drama", "Magic", "Sci-fi"],
    actor: [
      "Alexander Cattly",
      "Cartin Hollia",
      "Greta Garbo",
      "Humpray Richard",
      "Martin Brando",
    ],
    director: ["Grace Belly", "Kingia Rogers"],
    trailerUrl: "https://www.youtube.com/watch?v=TYMMOjBUPMM",
  },
  {
    id: "prison-break",
    title: "Prison Break",
    image: "/placeholder.svg?height=600&width=400&text=Prison+Break",
    rating: 8.2,
    duration: "01 hours 00 minutes",
    description:
      "Sed ut perspiciatis unde omnis iste natus error sit voluptatem...",
    language: "English",
    releaseDate: "May 5, 2022",
    genre: ["Cartoon", "Magic", "Sci-fi"],
    actor: [
      "Alexander Cattly",
      "Cartin Hollia",
      "Greta Garbo",
      "Martin Brando",
    ],
    director: ["Gally Peckin", "Grace Belly"],
    trailerUrl: "https://www.youtube.com/watch?v=AL9zLctDJaU",
  },
];

export default function ComingSoonPage() {
  const [selectedTrailer, setSelectedTrailer] = useState<string | null>(null);
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Hero Banner */}
      <div className="relative h-[300px] w-full">
        <Image
          src="https://media.istockphoto.com/id/1479991868/photo/theater-coming-soontext-background-3d-rendering.webp?a=1&b=1&s=612x612&w=0&k=20&c=Ui59IrxcxOQ4P6zAAJevjAOH9ukboeMg3Srk9vcEEDk="
          alt="Coming Soon Banner"
          fill
          className="object-cover"
        />
        <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
          <h1 className="text-4xl md:text-5xl font-bold text-white">
            Coming Soon
          </h1>
        </div>
      </div>

      {/* Movies Grid */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {upcomingMovies.map((movie) => (
            <div
              key={movie.id}
              className="bg-gray-800 rounded-lg overflow-hidden flex flex-col md:flex-row border border-gray-700 hover:border-gray-600 transition-colors"
            >
              {/* Movie Poster */}
              <div className="relative w-full md:w-[200px] h-[300px] md:h-[400px] flex-shrink-0">
                <Image
                  src={movie.image || "/placeholder.svg"}
                  alt={movie.title}
                  fill
                  className="object-cover"
                />
                <div className="absolute top-4 left-4 bg-orange-500 text-white rounded-full w-12 h-12 flex items-center justify-center">
                  <span className="text-lg font-bold">{movie.rating}</span>
                </div>
              </div>

              {/* Movie Details */}
              <div className="p-6 flex-1">
                <div className="flex items-start justify-between">
                  <h2 className="text-2xl font-bold mb-2 text-white">
                    {movie.title}
                  </h2>
                  <div className="flex items-center text-gray-400">
                    <Clock className="h-4 w-4 mr-1" />
                    <span className="text-sm">{movie.duration}</span>
                  </div>
                </div>

                <p className="text-gray-400 mb-4">{movie.description}</p>

                <div className="space-y-3">
                  <div className="text-gray-300">
                    <span className="font-semibold text-white">Language:</span>{" "}
                    {movie.language}
                  </div>
                  <div className="text-gray-300">
                    <span className="font-semibold text-white">
                      Release Date:
                    </span>{" "}
                    {movie.releaseDate}
                  </div>
                  <div>
                    <span className="font-semibold text-white">Genre:</span>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {movie.genre.map((g) => (
                        <Badge
                          key={g}
                          variant="secondary"
                          className="bg-gray-700 text-gray-200"
                        >
                          {g}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  <div className="text-gray-300">
                    <span className="font-semibold text-white">Actor:</span>
                    <p className="text-gray-400">{movie.actor.join(", ")}</p>
                  </div>
                  <div className="text-gray-300">
                    <span className="font-semibold text-white">Director:</span>
                    <p className="text-gray-400">{movie.director.join(", ")}</p>
                  </div>
                </div>

                <div className="flex gap-4 mt-6">
                  <Button
                    variant="default"
                    className="flex items-center bg-orange-500 hover:bg-orange-600"
                    onClick={() => setSelectedTrailer(movie.trailerUrl)}
                  >
                    <Play className="h-4 w-4 mr-2" />
                    Trailer
                  </Button>
                  <Button
                    variant="outline"
                    className="flex items-center border-gray-600 text-gray-200 hover:bg-gray-700"
                    onClick={() => router.push(`/movies/${movie.id}`)}
                  >
                    <Info className="h-4 w-4 mr-2" />
                    Detail
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Trailer Modal */}
      {selectedTrailer && (
        <div className="fixed inset-0 bg-black/90 flex items-center justify-center z-50 p-4">
          <div className="relative w-full max-w-4xl">
            <Button
              variant="ghost"
              size="icon"
              className="absolute -top-12 right-0 text-white hover:bg-white/20"
              onClick={() => setSelectedTrailer(null)}
            >
              <X className="h-6 w-6" />
            </Button>
            <div className="aspect-video relative">
              <ReactPlayer
                url={selectedTrailer}
                width="100%"
                height="100%"
                controls
                playing
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

"use client";

import { useState, useEffect, useRef } from "react";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { useRouter } from "next/navigation";
import { movies } from "@/lib/movies";
import axios from "axios";

// const allMovies = [
//   "The Shawshank Redemption",
//   "The Godfather",
//   "The Dark Knight",
//   "12 Angry Men",
//   "Schindler's List",
//   "Pulp Fiction",
//   "The Lord of the Rings: The Return of the King",
//   "The Good, the Bad and the Ugly",
//   "Fight Club",
//   "Forrest Gump",
// ];

export default function MovieSearch() {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredMovies, setFilteredMovies] = useState<any[]>([]);
  const [selectedMovies, setSelectedMovies] = useState<any[]>([]);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [allMovies, setAllMovies] = useState<String[]>()
  const dropdownRef = useRef<HTMLDivElement>(null);

  // filter movies titles from movies to create allMovies
  useEffect(() => {
    const getAllMovies = () => {
      axios.get('http://127.0.0.1:8000/movies/movies/').then((response) => {
        const movieTitles = response.data.map((movie: any) => movie.title);
        setAllMovies(movieTitles);
      }).catch(() => {
        setAllMovies([])
      })
    }
    // set allmovies
    getAllMovies();
  }, []);


  useEffect(() => {
    if (searchTerm) {
      const filtered = allMovies?.filter((movie) =>
        movie.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredMovies(filtered);
      setIsDropdownOpen(true);
    } else {
      setFilteredMovies([]);
      setIsDropdownOpen(false);
    }
  }, [searchTerm]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleMovieToggle = (movie: string) => {
    setSelectedMovies((prev) =>
      prev.includes(movie) ? prev.filter((m) => m !== movie) : [...prev, movie]
    );
  };

  const handleFindAndBook = () => {
    if (selectedMovies.length > 0) {
      const movieSlug = selectedMovies[0].toLowerCase().replace(/ /g, "-");
      router.push(`/movies/${movieSlug}`);
    }
  };

  return (
    <div className="flex flex-col sm:flex-row items-center space-y-2 sm:space-y-0 sm:space-x-2 w-full">
      <div className="relative w-full sm:w-64">
        <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Search movies..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-8 pr-4 py-2 rounded-md bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          aria-label="Search movies"
        />
        {isDropdownOpen && filteredMovies.length > 0 && (
          <div
            ref={dropdownRef}
            className="absolute z-10 mt-1 w-full bg-gray-700 rounded-md shadow-lg max-h-60 overflow-auto"
          >
            {filteredMovies.map((movie) => (
              <div
                key={movie}
                className="flex items-center space-x-2 p-2 hover:bg-gray-600"
              >
                <Checkbox
                  id={movie}
                  checked={selectedMovies.includes(movie)}
                  onCheckedChange={() => handleMovieToggle(movie)}
                />
                <label
                  htmlFor={movie}
                  className="text-sm text-gray-200 cursor-pointer"
                >
                  {movie}
                </label>
              </div>
            ))}
          </div>
        )}
      </div>
      <Button
        onClick={handleFindAndBook}
        disabled={selectedMovies.length === 0}
        className="w-full sm:w-auto"
      >
        Find Times & Book ({selectedMovies.length})
      </Button>
    </div>
  );
}

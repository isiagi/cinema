"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const slides = [
  {
    image: "https://assets.voxcinemas.com/content/Marco_1735722489.jpg",
    alt: "Movie 1",
    title: "Blockbuster Hit",
    description: "Experience the action-packed adventure of the year!",
  },
  {
    image:
      "https://assets.voxcinemas.com/content/Sonic-MP-SHARE--_1735197591.jpg",
    alt: "Movie 2",
    title: "Romantic Comedy",
    description: "Fall in love with the most heartwarming story of the season.",
  },
  {
    image:
      "https://assets.voxcinemas.com/content/DOT2_En_880x440-100_1735912459.jpg",
    alt: "Movie 3",
    title: "Sci-Fi Thriller",
    description: "Journey to the unknown in this mind-bending space odyssey.",
  },
];

export function Carousel() {
  const [currentSlide, setCurrentSlide] = useState(0);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  useEffect(() => {
    const timer = setInterval(nextSlide, 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="relative h-[400px] w-full overflow-hidden">
      {slides.map((slide, index) => (
        <div
          key={index}
          className={`absolute top-0 left-0 w-full h-full transition-opacity duration-1000 ${
            index === currentSlide ? "opacity-100" : "opacity-0"
          }`}
        >
          <Image
            src={slide.image || "/placeholder.svg"}
            alt={slide.alt}
            fill
            className="object-cover"
          />
          <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div className="text-center text-white">
              <h2 className="text-3xl font-bold mb-4">{slide.title}</h2>
              <p className="text-lg mb-8">{slide.description}</p>
              <Button size="lg">Book Now</Button>
            </div>
          </div>
        </div>
      ))}
      <Button
        variant="ghost"
        size="icon"
        className="absolute top-1/2 left-4 transform -translate-y-1/2 text-white"
        onClick={prevSlide}
      >
        <ChevronLeft size={24} />
      </Button>
      <Button
        variant="ghost"
        size="icon"
        className="absolute top-1/2 right-4 transform -translate-y-1/2 text-white"
        onClick={nextSlide}
      >
        <ChevronRight size={24} />
      </Button>
    </div>
  );
}

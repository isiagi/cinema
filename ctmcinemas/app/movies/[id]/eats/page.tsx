"use client";

import { useState } from "react";
import { useSearchParams, useRouter, useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Plus, Minus } from "lucide-react";

interface EatsItem {
  id: string;
  name: string;
  price: number;
  image: string;
}

const eatsItems: EatsItem[] = [
  {
    id: "popcorn",
    name: "Popcorn",
    price: 5000,
    image:
      "https://plus.unsplash.com/premium_photo-1676049461872-4f9703bdb732?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjV8fHBvcCUyMGNvcm58ZW58MHx8MHx8fDA%3D",
  },
  {
    id: "soda",
    name: "Soda",
    price: 3000,
    image:
      "https://images.unsplash.com/photo-1615568042524-3c8c5cb895d1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8c29kYSUyMGJvdHRsZXxlbnwwfHwwfHx8MA%3D%3D",
  },
  {
    id: "nachos",
    name: "Nachos",
    price: 7000,
    image:
      "https://plus.unsplash.com/premium_photo-1690440686714-c06a56a1511c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8aWNlJTIwY3JlYW18ZW58MHx8MHx8fDA%3D",
  },
  {
    id: "hotdog",
    name: "Hot Dog",
    price: 6000,
    image:
      "https://images.unsplash.com/photo-1627054248949-21f77275a15f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fGhvdCUyMGRvZ3xlbnwwfHwwfHx8MA%3D%3D",
  },
];

export default function EatsPage() {
  const searchParams = useSearchParams();
  const params = useParams();
  const router = useRouter();
  const [selectedEats, setSelectedEats] = useState<Record<string, number>>({});

  const movieId = params.id;
  const date = searchParams.get("date");
  const time = searchParams.get("time");
  const seats = searchParams.get("seats");

  const handleQuantityChange = (itemId: string, change: number) => {
    setSelectedEats((prev) => {
      const newQuantity = (prev[itemId] || 0) + change;
      if (newQuantity <= 0) {
        const { [itemId]: _, ...rest } = prev;
        return rest;
      }
      return { ...prev, [itemId]: newQuantity };
    });
  };

  const totalPrice = Object.entries(selectedEats).reduce(
    (total, [itemId, quantity]) => {
      const item = eatsItems.find((i) => i.id === itemId);
      return total + (item?.price || 0) * quantity;
    },
    0
  );

  const handleContinue = () => {
    const eatsParam = Object.entries(selectedEats)
      .map(([itemId, quantity]) => `${itemId}:${quantity}`)
      .join(",");
    router.push(
      `/movies/${movieId}/summary?date=${date}&time=${time}&seats=${seats}&eats=${eatsParam}`
    );
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8">Select Your Eats</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {eatsItems.map((item) => (
          <div
            key={item.id}
            className="flex items-center space-x-4 p-4 border rounded-lg"
          >
            <img
              src={item.image || "/placeholder.svg"}
              alt={item.name}
              className="w-20 h-20 object-cover rounded"
            />
            <div className="flex-grow">
              <h3 className="text-lg font-semibold">{item.name}</h3>
              <p className="text-gray-600">{item.price.toLocaleString()} UGX</p>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                size="sm"
                variant="outline"
                onClick={() => handleQuantityChange(item.id, -1)}
                disabled={!selectedEats[item.id]}
              >
                <Minus className="h-4 w-4" />
              </Button>
              <Input
                type="number"
                min="0"
                value={selectedEats[item.id] || 0}
                onChange={(e) => {
                  const newQuantity = Number.parseInt(e.target.value) || 0;
                  setSelectedEats((prev) => ({
                    ...prev,
                    [item.id]: newQuantity,
                  }));
                }}
                className="w-16 text-center"
              />
              <Button
                size="sm"
                variant="outline"
                onClick={() => handleQuantityChange(item.id, 1)}
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-between items-center mb-8">
        <p className="text-xl font-bold">
          Total: {totalPrice.toLocaleString()} UGX
        </p>
        <Button onClick={handleContinue}>Continue to Summary</Button>
      </div>
    </div>
  );
}

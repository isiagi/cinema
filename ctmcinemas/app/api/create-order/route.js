import { NextResponse } from "next/server";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export async function POST(request) {
  console.log("Creating order...cccccc");

  const body = await request.json();
  const { userId, movieId, date, time, seats, eats, totalPrice } = body;

  try {
    const showing = await prisma.showing.findFirst({
      where: {
        movieId,
        date: new Date(date),
        time,
      },
    });

    if (!showing) {
      return NextResponse.json({ error: "Showing not found" }, { status: 404 });
    }

    const order = await prisma.order.create({
      data: {
        userId,
        showingId: showing.id,
        seats,
        eats,
        totalPrice,
      },
    });

    return NextResponse.json(order);
  } catch (error) {
    console.error("Error creating order:", error);
    return NextResponse.json(
      { error: "Failed to create order" },
      { status: 500 }
    );
  }
}

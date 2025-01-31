import { auth } from "@clerk/nextjs/server";
import { PrismaClient } from "@prisma/client";
import { Button } from "@/components/ui/button";
import Link from "next/link";

const prisma = new PrismaClient();

async function getOrders(userId: string) {
  const orders = await prisma.order.findMany({
    where: { userId },
    include: {
      showing: {
        include: {
          movie: true,
        },
      },
    },
    orderBy: {
      createdAt: "desc",
    },
  });
  return orders;
}

export default async function OrdersPage() {
  const { userId } = await auth();

  if (!userId) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <h1 className="text-2xl font-bold mb-4">
          Please log in to view your orders
        </h1>
        <Link href="/login">
          <Button>Log In</Button>
        </Link>
      </div>
    );
  }

  const orders = await getOrders(userId);

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8">Your Orders</h1>
      {orders.length === 0 ? (
        <p>You haven't made any orders yet.</p>
      ) : (
        <div className="space-y-8">
          {orders.map((order) => (
            <div key={order.id} className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">
                {order.showing.movie.title}
              </h2>
              <p>Date: {new Date(order.showing.date).toLocaleDateString()}</p>
              <p>Time: {order.showing.time}</p>
              <p>Seats: {order.seats.join(", ")}</p>
              <p>
                Eats:
                {Object.entries(order.eats as Record<string, number>)
                  .map(([item, quantity]) => `${item} (${quantity})`)
                  .join(", ")}
              </p>
              <p className="font-bold mt-2">
                Total Price: {order.totalPrice.toLocaleString()} UGX
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

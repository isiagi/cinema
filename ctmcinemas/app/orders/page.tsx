/* eslint-disable @typescript-eslint/no-explicit-any */

export default async function OrdersPage() {
  // if (!userId) {
  //   return (
  //     <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
  //       <h1 className="text-2xl font-bold mb-4">
  //         Please log in to view your orders
  //       </h1>
  //       <Link href="/login">
  //         <Button>Log In</Button>
  //       </Link>
  //     </div>
  //   );
  // }

  const orders = [];

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8">Your Orders</h1>
      {orders.length === 0 ? (
        <p>You haven&apos;t made any orders yet.</p>
      ) : (
        <div className="space-y-8">
          {[].map((order: any) => (
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

import { Button } from "@/components/ui/button";
import {
  ArrowRight,
  Film,
  Users,
  UserPlus,
  Baby,
  PartyPopper,
} from "lucide-react";
import Link from "next/link";

const services = [
  {
    icon: Film,
    title: "Movie Screening",
    description:
      "Experience the latest blockbusters in state-of-the-art theatres.",
  },
  {
    icon: Users,
    title: "Theatre Rental",
    description:
      "Rent our theatres for corporate events or private gatherings.",
  },
  {
    icon: UserPlus,
    title: "Private Screening",
    description: "Enjoy exclusive screenings with your friends and family.",
  },
  {
    icon: Baby,
    title: "Kids Entertainment",
    description:
      "Special screenings and events tailored for our younger audience.",
  },
  {
    icon: PartyPopper,
    title: "Special Events",
    description: "Host premieres, festivals, and themed movie nights.",
  },
];

export function ServicesSection() {
  return (
    <section className="bg-gray-100 py-16">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12">Our Services</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-md">
              <service.icon className="w-12 h-12 text-blue-500 mb-4" />
              <h3 className="text-xl font-semibold mb-2">{service.title}</h3>
              <p className="text-gray-600 mb-4">{service.description}</p>
            </div>
          ))}
        </div>
        <div className="text-center mt-12">
          <Link href="/services">
            <Button className="bg-blue-500 hover:bg-blue-600">
              View All Services <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}

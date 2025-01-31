import { Carousel } from "@/components/Carousel";
import { ServicesSection } from "@/components/ServicesSection";
import { WhatsOn } from "@/components/WhatsOn";

export default function Home() {
  return (
    <main>
      <Carousel />
      <WhatsOn />
      <ServicesSection />
    </main>
  );
}

import Link from "next/link";
import { Facebook, Instagram, Twitter } from "lucide-react";

export function TopBanner() {
  return (
    <div className="bg-gray-900 text-white py-2 px-4">
      <div className="container mx-auto flex justify-between items-center text-sm">
        <div>Open: Mon-Sun 10AM-10PM</div>
        <div>Contact: 0200916821</div>
        <div className="flex space-x-4">
          <Link
            href="https://www.facebook.com/profile.php?id=61568398119994&mibextid=ZbWKwL"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Facebook size={16} />
          </Link>
          <Link
            href="https://www.instagram.com/emtcinemas?igsh=MWdnaDd0MXF5bGcwZQ=="
            target="_blank"
            rel="noopener noreferrer"
          >
            <Instagram size={16} />
          </Link>
          <Link
            href="https://x.com/emtcinemas?t=lAI3J827gaZbDJt_am74vA&s=09"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Twitter size={16} />
          </Link>
        </div>
      </div>
    </div>
  );
}

"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Film, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import MovieSearch from "./MovieSearch";
import { UserButton, SignInButton, useUser } from "@clerk/nextjs";
import AuthModal from "./signinup";
import axios from "axios";
import PopupMessage from "./popup";

export default function Navbar() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  // const { isSignedIn, user } = useUser();
  const [user, setUser] = useState<any>({})
  const [openUp, setOpenUp] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [color, setColor] = useState<string>("");
  const [bgColor, setBgColor] = useState<string>("");
  const [popupMessage, setPopupMessage] = useState("");
  const access_token = localStorage.getItem('access_token');
  const refresh_token = localStorage.getItem("refresh_token");

  useEffect(() => {
    const getUserProfile = () => {
      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:8000/auth/profile/',
        headers: {
          'Authorization': `Bearer ${access_token}`
        }
      };

      axios.request(config).then((response) => {
        setUser(response.data);
      }).catch((error) => {
        setUser({})
        console.log(error.response.data)
      });
    }

    getUserProfile()


    const handleScroll = () => {
      // Get banner height (400px) plus any additional spacing
      const bannerHeight = 400;
      setIsScrolled(window.scrollY > bannerHeight);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);

  }, []);

  const handleLogout = async () => {
    if (!refresh_token) {
      setColor("red-800")
      setBgColor("red-200")
      setPopupMessage("No refresh token found.");
      return;
    }

    try {
      await axios.post("http://127.0.0.1:8000/auth/logout/", {}, {
        headers: {
          refresh: refresh_token,
          access: access_token
        }
      });

      // Clear tokens from local storage
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      // Clear user state and close dropdown
      setUser({});
      setIsDropdownOpen(false);

      setColor("green-800")
      setBgColor("green-200")
      setPopupMessage("Logout successful");
    } catch (error: any) {
      setUser({});
      console.error("Logout failed", error.response?.data);
    }
  };

  return (
    <nav className={`w-full transition-all duration-300 ${ isScrolled ? "fixed top-0 bg-gray-800 shadow-lg z-50" : "bg-gray-800" }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0">
              <Film className="h-8 w-8 text-white" />
            </Link>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link href="/whatson" className="text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
                  What's On
                </Link>
                <Link href="/comingsoon" className="text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
                  Coming Soon
                </Link>
                <Link href="/eats" className="text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
                  Eats
                </Link>
              </div>
            </div>
          </div>
          <div className="hidden md:flex items-center space-x-4">
            <MovieSearch />
            {user && user.is_active ? (
              <div className="relative">
                <Button className="text-black text-sm mr-2 border bg-gray-400 rounded-full w-11 h-11 flex justify-center items-center font-extrabold" onClick={() => setIsDropdownOpen(!isDropdownOpen)}>
                  {user.name.slice(0,3)}
                </Button>

                {/* Dropdown Menu */}
                {isDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-52 bg-white rounded-lg shadow-lg border z-50">
                    <div className="p-3 border-b">
                      <p className="font-semibold text-gray-800">{user.name}</p>
                      <p className="text-sm text-gray-500">{user.email}</p>
                    </div>
                    <button className="block w-full text-center bg-red-500 text-white py-2 rounded-b-lg hover:bg-red-600" onClick={handleLogout}>
                      Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <Button variant="outline" size="sm" className="border-white hover:bg-white text-blue-800" onClick={() => setOpenUp(true)}>
                Sign In
              </Button>
            )}
          </div>
          <div className="-mr-2 flex md:hidden">
            <Button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white">
              <span className="sr-only">Open main menu</span>
              {isMobileMenuOpen ? (
                <X className="block h-6 w-6" aria-hidden="true" />
              ) : (
                <Menu className="block h-6 w-6" aria-hidden="true" />
              )}
            </Button>
          </div>
        </div>
      </div>

      {isMobileMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <Link href="/whatson" className="text-white hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium">
              What's On
            </Link>
            <Link href="/comingsoon" className="text-white hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium">
              Coming Soon
            </Link>
            <Link href="/eats" className="text-white hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium">
              Eats
            </Link>
          </div>
          <div className="pt-4 pb-3 border-t border-gray-700">
            <div className="px-2 space-y-1">
              <MovieSearch />
              {user && user.is_active ? (
                <div className="flex items-center px-3 py-2">
                  <span className="text-gray-300 text-sm mr-2">
                    Signed in as {user.name}
                  </span>
                  <UserButton afterSignOutUrl="/" />
                </div>
              ) : (
                <Button variant="outline" size="sm" className="w-full text-white border-white hover:bg-white hover:text-gray-800" onClick={() => setOpenUp(true)}>
                  Sign In
                </Button>
              )}
            </div>
          </div>
        </div>
      )}

      <AuthModal isOpen={openUp} onClose={() => setOpenUp(false)} />
      {popupMessage && <PopupMessage color={color} bgColor={bgColor} message={popupMessage} onClose={() => setPopupMessage("")} />}
    </nav>
  );
}

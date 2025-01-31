import { useEffect, useState } from "react";

const PopupMessage = ({ color, message, bgColor, onClose }: any) => {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      if (onClose) onClose();
    }, 3000); // Auto-hide after 3 seconds

    return () => clearTimeout(timer);
  }, [onClose]);

  if (!visible) return null;

  return (
    <div className={`fixed top-5 right-5 border-0 border-l-2 border-[${color}] bg-[${bgColor}] text-white px-6 py-3 rounded-sm shadow-lg transition-all animate-fadeIn z-50`}>
      {message}
    </div>
  );
};

export default PopupMessage;

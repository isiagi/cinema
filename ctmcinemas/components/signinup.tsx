import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
// import { Label } from "@/components/ui/label";
import { login, register, resetPassword, forgot_password } from "@/types/api";
import PopupMessage from "./popup";

export default function AuthModal({ isOpen, onClose }: any) {
    const [tab, setTab] = useState("login");
    const [formData, setFormData] = useState({ email: "", password: "", username: "" });
    const [errors, setErrors] = useState({ email: "", password: "", username: "" });
    const [showPassword, setShowPassword] = useState(false);
    const [forgotPassword, setForgotPassword] = useState(false);
    const [resetEmail, setResetEmail] = useState("");
    const [isResetModalOpen, setIsResetModalOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const [color, setColor] = useState<string>("");
    const [bgColor, setBgColor] = useState<string>("");
    const [popupMessage, setPopupMessage] = useState("");

    // Handle input changes
    const handleChange = (e: any) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        setErrors({ ...errors, [e.target.name]: "" });
    };

    const handleSubmit = async (action: string) => {
        setLoading(true);
        let newErrors = { email: "", password: "", username: "" };

        if (!formData.email) {
            newErrors.email = "Email is required";
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = "Enter a valid email";
        }

        if (!formData.password) {
            newErrors.password = "Password is required";
        } else if (formData.password.length < 1) {
            newErrors.password = "Password cannot be empty";
        }

        if (tab === "register" && !formData.username) {
            newErrors.username = "Username is required";
        }

        setErrors(newErrors);

        if (Object.values(newErrors).some((err) => err)) {
            setLoading(false);
            return;
        }

        try {
            let response;
            if (action === "login") {
                response = await login(formData.email, formData.password);
                setPopupMessage("Login successful.")
                
                localStorage.setItem("access_token", response.data.access);
                localStorage.setItem("refresh_token", response.data.refresh);
                setFormData({ email: "", password: "", username: "" });
                window.location.reload();
            } else if (action === "register") {
                response = await register({email: formData.email, password: formData.password, name: formData.username});
                setPopupMessage("Registration successful.")
            }

            setColor("#62a03f");
            setBgColor("#111827");
            setTimeout(() => onClose(), 1000)
        } catch (error) {
            console.error("Error:", error);
            setErrors((prev) => ({ ...prev, email: "Invalid credentials or server error" }));
        } finally {
            setLoading(false);
        }
    };

    const handlePasswordReset = async (e: any) => {
        e.preventDefault();
        setLoading(true);

        if (!resetEmail) {
            setErrors({ ...errors, email: "Enter your email" });
            setLoading(false);
            return;
        }

        try {
            await forgot_password(resetEmail);
            console.log("Password reset email sent to:", resetEmail);
            setIsResetModalOpen(false);
        } catch (error) {
            console.error("Error:", error);
            setErrors({ ...errors, email: "Failed to send reset link" });
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            {/* Main Auth Modal */}
            <Dialog open={isOpen} onOpenChange={onClose}>
                <DialogContent className="max-w-md">
                    <DialogHeader>
                        <DialogTitle>
                            {forgotPassword ? (
                                "Forgot Password"
                            ) : (
                                <div className="flex justify-around pb-2">
                                    <button className={`w-1/2 p-2 text-center ${tab === "login" ? "border-b-2 border-blue-500 font-semibold" : "text-gray-500"}`} onClick={() => setTab("login")}>
                                        Sign In
                                    </button>
                                    <button className={`w-1/2 p-2 text-center ${tab === "register" ? "border-b-2 border-blue-500 font-semibold" : "text-gray-500"}`} onClick={() => setTab("register")}>
                                        Register
                                    </button>
                                </div>
                            )}
                        </DialogTitle>
                    </DialogHeader>

                    {/* Forgot Password UI */}
                    {forgotPassword ? (
                        <form className="space-y-4 p-4">
                            <h5>Email</h5>
                            <Input type="email" name="resetEmail" placeholder="Enter your email" value={resetEmail} onChange={(e) => setResetEmail(e.target.value)} required />
                            {errors.email && <p className="text-red-500 text-sm">{errors.email}</p>}

                            <Button onClick={handlePasswordReset} className="w-full">Send Reset Link</Button>
                            <p className="text-center text-sm text-gray-500 cursor-pointer" onClick={() => setForgotPassword(false)}>
                                Back to Login
                            </p>
                        </form>
                    ) : (
                        <form className="space-y-4 p-4">
                            {tab === "register" && (
                                <div>
                                    <h5>Username</h5>
                                    <Input type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required />
                                    {errors.username && <p className="text-red-500 text-sm">{errors.username}</p>}
                                </div>
                            )}

                            <div>
                                <h5>Email</h5>
                                <Input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
                                {errors.email && <p className="text-red-500 text-sm">{errors.email}</p>}
                            </div>

                            <div className="relative">
                                <h5>Password</h5>
                                <Input type={showPassword ? "text" : "password"} name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
                                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-9 text-gray-500">
                                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                                </button>
                                {errors.password && <p className="text-red-500 text-sm">{errors.password}</p>}
                            </div>

                            {tab === "login" && (
                                <p className="text-sm text-blue-500 cursor-pointer text-right" onClick={() => setForgotPassword(true)}>
                                    Forgot password?
                                </p>
                            )}

                            {tab === "login" ?
                                <Button className="w-full" onClick={() => handleSubmit('login')} disabled={loading}>
                                    {loading ? "loading......." : "Sign In"}
                                </Button>
                            :
                                <Button className="w-full" onClick={() => handleSubmit('register')} disabled={loading}>
                                    {loading ? "loading......." : "Register"}
                                </Button>
                            }
                        </form>
                    )}
                </DialogContent>
            </Dialog>

            {/* Reset Password Modal */}
            <Dialog open={isResetModalOpen} onOpenChange={setIsResetModalOpen}>
                <DialogContent className="max-w-md">
                    <DialogHeader>
                        <DialogTitle>Reset Password</DialogTitle>
                    </DialogHeader>
                    <form onSubmit={handlePasswordReset} className="space-y-4 p-4">
                        <h5>Email</h5>
                        <Input type="email" name="resetEmail" placeholder="Enter your email" value={resetEmail} onChange={(e) => setResetEmail(e.target.value)} required />
                        {errors.email && <p className="text-red-500 text-sm">{errors.email}</p>}

                        <Button className="w-full">Send Reset Link</Button>
                    </form>
                </DialogContent>
            </Dialog>

            {popupMessage && <PopupMessage color={color} bgColor={bgColor} message={popupMessage} onClose={() => setPopupMessage("")} />}
        </>
    );
}

import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { useUser } from "../contexts/UserContext";

const UserLogin = () => {
  const navigate = useNavigate();
  const { setUser } = useUser();

  return (
    <GoogleOAuthProvider clientId="489112235114-tl5r1a1451nva666af8kbdrevjkrmkoi.apps.googleusercontent.com">
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="bg-white shadow-md rounded-lg p-8 w-96">
          <h2 className="text-2xl font-semibold text-center mb-6 text-gray-800">
            Login
          </h2>
          <GoogleLogin
            onSuccess={(credentialResponse) => {
              const credentialResponseDecoded = jwtDecode(
                credentialResponse.credential
              );
              setUser([credentialResponseDecoded, null]);

              fetch("http://election.zapto.org/voter/signin", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify(credentialResponseDecoded),
              })
                .then((response) => response.json()) // Extract JSON
                .then((data) => {
                  const accessToken = data.access_token;
                  console.log(accessToken);

                  setUser([credentialResponseDecoded, accessToken]);

                  localStorage.setItem(
                    "User",
                    JSON.stringify([credentialResponseDecoded, accessToken])
                  );

                  toast.success("Login Successful!");
                  navigate("/voter/polls");
                })
                .catch((error) => {
                  console.error("Error during login:", error);
                  toast.error("Login Failed");
                });
            }}
            onError={() => {
              console.log("Login Failed");
              toast.error("Login Failed");
            }}
            className="w-full"
          />
        </div>
      </div>
    </GoogleOAuthProvider>
  );
};

export default UserLogin;

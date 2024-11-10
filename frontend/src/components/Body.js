import { Link } from "react-router-dom";
import { useUser } from "../contexts/UserContext";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
const Body = () => {
  const { user, setUser } = useUser();
  const navigate = useNavigate();

  return (
    <div className="mt-32 w-full h-screen flex justify-center bg-white text-gray-800">
      <div className="text-center p-4 max-w-4xl space-y-10">
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold">
          Election Management Made Simple, and Transparent
        </h1>
        {/* Explore Button */}
        <div className="flex items-center justify-center">
          {user ? (
            <Link to="/voter/polls">
              <button className="explore-btn flex items-center justify-center space-x-2 py-4 px-12 text-xl bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors duration-300 ease-in-out">
                <span>Explore</span>
                <span>&#8594;</span> {/* Right Arrow */}
              </button>
            </Link>
          ) : (
            <Link to="/voter/login">
              <button className="explore-btn flex items-center justify-center space-x-2 py-4 px-12 text-xl bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors duration-300 ease-in-out">
                <span>Explore</span>
                <span>&#8594;</span> {/* Right Arrow */}
              </button>
            </Link>
          )}
        </div>
      </div>
    </div>
  );
};

export default Body;

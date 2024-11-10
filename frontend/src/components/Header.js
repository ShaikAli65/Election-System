import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import { useUser } from "../contexts/UserContext";

const Header = () => {
  const { user, setUser } = useUser();
  let userName;
  if (user != null) {
    userName = user[0].given_name;
  }

  return (
    <div className="header container mx-auto px-6 py-4 flex justify-between items-center bg-white shadow-md">
      {/* Logo Section */}
      <Link to="/">
        <div className="logo text-2xl font-bold text-gray-800 hover:text-blue-600 transition-colors duration-300 ease-in-out">
          LOGO
        </div>
      </Link>

      {/* Navigation Links */}
      <div className="flex items-center space-x-6">
        {/* Polls Link with Hover Effects */}
        <Link to="/voter/polls">
          <div className="polls text-lg text-white bg-blue-500 hover:bg-blue-600 px-6 py-2 rounded-md transition-all duration-300 ease-in-out cursor-pointer">
            View Polls
          </div>
        </Link>

        {/* User Icon Section */}
        <Link to="/voter/login">
          <div className="user-icon-div">
            {user ? (
              <span className="text-red-500 text-lg font-bold">
                Hello, {userName}
              </span>
            ) : (
              <FontAwesomeIcon
                icon={faUser}
                className="user-icon text-gray-700 text-2xl hover:text-blue-500 transition-colors duration-300 ease-in-out"
              />
            )}
          </div>
        </Link>
      </div>
    </div>
  );
};

export default Header;

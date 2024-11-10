import { Link } from "react-router-dom";
const DisplayPollVoter = ({ data }) => {
  const formatDate = (isoString) => {
    const date = new Date(isoString);
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    }).format(date);
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 max-w-md mx-auto my-6">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">
        Election Name: <span className="text-blue-600">{data.title}</span>
      </h1>
      <h3 className="text-lg text-gray-700 mb-2 flex justify-between">
        <span className="font-semibold">Election Start Date:</span>
        <span className="text-gray-600">{formatDate(data.start_date)}</span>
      </h3>
      <h3 className="text-lg text-gray-700 mb-2 flex justify-between">
        <span className="font-semibold">Election End Date:</span>
        <span className="text-gray-600">{formatDate(data.end_date)}</span>
      </h3>
      <h3 className="text-lg text-gray-700 mb-4 flex justify-between">
        <span className="font-semibold">Election Status:</span>
        <span
          className={`font-semibold ${
            data.election_status === "upcoming"
              ? "text-green-600"
              : "text-red-600"
          }`}
        >
          {data.election_status}
        </span>
      </h3>
      <Link to={`/voter/poll/${data.election_id}`}>
        <button className="mt-4 bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 transition duration-200 ease-in-out">
          More Details
        </button>
      </Link>
    </div>
  );
};

export default DisplayPollVoter;

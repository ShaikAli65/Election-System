import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { useUser } from "../contexts/UserContext";
const DisplayPollComplete = () => {
  const { user, setUser } = useUser();
  const { poll_id } = useParams();
  const [pollData, setPollData] = useState(null);
  const [loading, setLoading] = useState(false); // State to store poll data
  console.log(user);
  useEffect(() => {
    const fetchPollData = async () => {
      try {
        const response = await fetch(
          `http://election.zapto.org/admin/polls/${poll_id}`
        );

        if (!response.ok) {
          throw new Error("Failed to fetch poll data");
        }

        const data = await response.json();
        console.log(data);

        setPollData(data); // Update the state with the fetched data
      } catch (err) {
        console.log(err.message); // Capture any errors
      }
    };

    // Fetch poll data when poll_id is available
    if (poll_id) {
      fetchPollData();
    }
  }, [poll_id]);
  if (!pollData) {
    return <div>HELLo</div>;
  }
  const {
    title,
    description,
    start_date,
    end_date,
    validation_regex,
    candidates,
  } = pollData;

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Poll Info Section */}
      <div className="bg-white p-8 rounded-lg shadow-lg mb-8 max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-blue-600 mb-6">{title}</h1>
        <p className="text-lg text-gray-700 mb-4">{description}</p>
        <div className="space-y-3">
          <p className="text-lg text-gray-600">
            <strong className="text-gray-700 text-xl">Start Date:</strong>
            <span className="text-gray-800 ml-4">
              {new Date(start_date).toLocaleString()}
            </span>
          </p>
          <p className="text-lg text-gray-600">
            <strong className="text-gray-700 text-xl">End Date:</strong>
            <span className="text-gray-800 ml-4">
              {new Date(end_date).toLocaleString()}
            </span>
          </p>
          <p className="text-lg text-gray-600">
            <strong className="text-gray-700 text-xl">Validation Regex:</strong>
            <span className="text-gray-800 ml-4">{validation_regex}</span>
          </p>
        </div>
      </div>

      {/* Candidates Section */}
      <div>
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          Candidates
        </h2>
        <ul className="space-y-4">
          {candidates.map((candidate) => (
            <li
              key={candidate.candidateId}
              className="bg-gray-100 p-4 rounded-lg shadow-sm"
            >
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {candidate.candidate_name}
              </h3>
              <p className="text-md text-gray-600 mb-1">
                <strong>Email:</strong> {candidate.email_id}
              </p>
              <p className="text-md text-gray-600 mb-1">
                <strong>Manifesto:</strong>{" "}
                <a
                  href={`http://election.zapto.org/portfolio/?pollId=ec4b82e9-22d8-4eb6-8319-8fb5bc4fd47d&candidateId=${candidate.candidateId}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:text-blue-700"
                  download // This will trigger the download behavior
                >
                  View Manifesto
                </a>
              </p>

              <p className="text-md text-gray-600 mb-1">
                <strong>Word from Candidate:</strong>{" "}
                {candidate.word_from_candidate}
              </p>
              <p className="text-md text-gray-600 mb-1">
                <strong>Total Votes:</strong> {candidate.total_votes}
              </p>
              <p className="text-sm text-gray-500">
                <strong>Nomination Date:</strong>{" "}
                {new Date(candidate.nomination_date).toLocaleString()}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default DisplayPollComplete;

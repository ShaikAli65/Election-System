import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { useUser } from "../contexts/UserContext";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const DisplayPollCompleteVoter = () => {
  const { user } = useUser();
  const { poll_id } = useParams();
  const [pollData, setPollData] = useState(null);
  const [loading, setLoading] = useState(false);
  const handleJoinPoll = async () => {
    // Logic to join the poll, e.g., sending a request to the server
    const response = await fetch(
      `http://election.zapto.org/voter/joinrequest/${poll_id}`,
      {
        method: "POST",
        headers: {
          access_token: user[1],
        },
      }
    );

    if (response.status === 406) {
      toast.error("Candidate already registered");
    } else if (response.ok) {
      // Successful response
      toast.success("Successfully joined the poll!");
    } else {
      // Handle other error statuses or unexpected responses
      toast.error("Something went wrong. Please try again.");
    }
  };
  useEffect(() => {
    const fetchPollData = async () => {
      try {
        const response = await fetch(
          `http://election.zapto.org/voter/poll/${poll_id}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              access_token: user[1],
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch poll data");
        }

        const data = await response.json();
        console.log(data);

        setPollData(data);
      } catch (err) {
        console.log(err.message);
      }
    };

    if (poll_id) {
      fetchPollData();
    }
  }, [poll_id]);

  const handleVote = async (candidateId) => {
    const confirmVote = window.confirm("Are you sure?");
    if (!confirmVote) return;

    try {
      const formData = new FormData();
      console.log(candidateId);

      formData.append("candidate_id", candidateId);
      formData.append("poll_id", poll_id);
      console.log(candidateId);
      console.log(poll_id);
      const response = await fetch(`http://election.zapto.org/voter/castVote`, {
        method: "POST",
        headers: {
          access_token: user[1],
        },
        body: formData,
      });

      if (response.status === 406) {
        toast.error("Vote could not be accepted. Please try again.");
      } else if (!response.ok) {
        throw new Error("Failed to cast vote");
      } else {
        const result = await response.json();
        toast.success("Vote cast successfully!");
      }
    } catch (err) {
      console.log(err.message);
      toast.error("An error occurred while casting your vote.");
    }
  };

  if (!pollData) {
    return <div>Loading poll data...</div>;
  }

  const { title, description, start_date, end_date, candidates, is_joined } =
    pollData;

  return (
    <div className="max-w-4xl mx-auto p-4">
      <ToastContainer />
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
        </div>
        <div>
          {!is_joined ? (
            <button
              className="mt-6 px-6 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold shadow-md"
              onClick={handleJoinPoll}
            >
              Join Poll
            </button>
          ) : null}
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
                  href={`http://election.zapto.org/portfolio/?pollId=${poll_id}&candidateId=${candidate.candidate_id}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:text-blue-700"
                  download
                >
                  View Manifesto
                </a>
              </p>
              <p className="text-md text-gray-600 mb-1">
                <strong>Word from Candidate:</strong>{" "}
                {candidate.word_from_candidate}
              </p>
              <p className="text-sm text-gray-500">
                <strong>Nomination Date:</strong>{" "}
                {new Date(candidate.nomination_date).toLocaleString()}
              </p>
              <button
                className="mt-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
                onClick={() => handleVote(candidate.candidate_id)}
              >
                Vote
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default DisplayPollCompleteVoter;

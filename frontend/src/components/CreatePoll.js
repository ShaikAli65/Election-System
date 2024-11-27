import { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
function PollForm() {
  const [pollName, setPollName] = useState("");
  const [pollDescription, setPollDescription] = useState(""); // State for poll description
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [validation, setValidation] = useState(""); // New state for validation
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  // Handler to add a new candidate
  const addCandidate = () => {
    setCandidates([...candidates, { name: "", email: "", word: "" }]);
  };

  // Handler to delete a candidate
  const deleteCandidate = (index) => {
    const newCandidates = candidates.filter((_, i) => i !== index);
    setCandidates(newCandidates);
  };
  // Handler to update candidate information
  const handleCandidateChange = (index, field, value) => {
    const newCandidates = [...candidates];
    newCandidates[index][field] = value;
    setCandidates(newCandidates);
  };

  // Handler for submitting form data
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append("title", pollName);
    formData.append("description", pollDescription); // Append poll description
    formData.append("start_date", startDate);
    formData.append("end_date", endDate);
    formData.append("validation_regex", validation); // Append validation

    candidates.forEach((candidate, index) => {
      const myUUID = uuidv4();
      console.log(myUUID);

      formData.append(`candidates{${myUUID}}{candidate_id}`, myUUID);
      formData.append(`candidates{${myUUID}}{candidate_name}`, candidate.name);
      formData.append(`candidates{${myUUID}}{email_id}`, candidate.email);
      formData.append(
        `candidates{${myUUID}}{word_from_candidate}`,
        candidate.word
      ); // Append candidate's word
      if (candidate.portfolio) {
        formData.append(
          `candidates{${myUUID}}{portfolio}`,
          candidate.portfolio
        );
      }
    });
    console.log(formData);
    try {
      const response = await fetch(
        "http://election.zapto.org/admin/createPoll",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log("Poll created successfully:", data);
      toast.success("Poll created successfully!");
      navigate("/admin/polls");
    } catch (error) {
      toast.error("Poll creation failed!");
      console.error("Error creating poll:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {loading ? (
        <div className="flex flex-col justify-center items-center">
          {/* Tailwind Spinner */}
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="mt-2 text-gray-700">Submitting your poll...</p>
        </div>
      ) : (
        <form
          onSubmit={handleSubmit}
          className="m-2 max-w-2xl mx-auto bg-gray-100 p-8 shadow-md rounded-md"
        >
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            Create Poll Form
          </h2>

          <div className="mb-4">
            <label className="block text-gray-800 font-medium mb-1">
              Poll Name:
            </label>
            <input
              type="text"
              value={pollName}
              onChange={(e) => setPollName(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-800 font-medium mb-1">
              Description:
            </label>
            <textarea
              value={pollDescription}
              onChange={(e) => setPollDescription(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-800 font-medium mb-1">
              Validation:
            </label>
            <input
              type="text"
              value={validation}
              onChange={(e) => setValidation(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-gray-800 font-medium mb-1">
                Start Date & Time:
              </label>
              <input
                type="datetime-local"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
            </div>
            <div>
              <label className="block text-gray-800 font-medium mb-1">
                End Date & Time:
              </label>
              <input
                type="datetime-local"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
            </div>
          </div>

          <h3 className="text-xl font-medium text-gray-900 mb-4">Candidates</h3>
          <button
            type="button"
            onClick={addCandidate}
            className="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300"
          >
            Add Candidate
          </button>

          {candidates.map((candidate, index) => (
            <div
              key={index}
              className="border border-gray-300 rounded-lg p-4 mb-4 bg-white relative"
            >
              <h4 className="text-lg font-semibold text-gray-700 mb-2">
                Candidate {index + 1}
              </h4>

              <div className="mb-3">
                <label className="block text-gray-700 font-medium mb-1">
                  Name:
                </label>
                <input
                  type="text"
                  value={candidate.name}
                  onChange={(e) =>
                    handleCandidateChange(index, "name", e.target.value)
                  }
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-300"
                />
              </div>

              <div className="mb-3">
                <label className="block text-gray-700 font-medium mb-1">
                  Email:
                </label>
                <input
                  type="email"
                  value={candidate.email}
                  onChange={(e) =>
                    handleCandidateChange(index, "email", e.target.value)
                  }
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-300"
                />
              </div>

              <div className="mb-3">
                <label className="block text-gray-700 font-medium mb-1">
                  Word:
                </label>
                <textarea
                  value={candidate.word}
                  onChange={(e) =>
                    handleCandidateChange(index, "word", e.target.value)
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-300"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-medium mb-1">
                  Portfolio:
                </label>
                <input
                  type="file"
                  onChange={(e) =>
                    handleCandidateChange(index, "portfolio", e.target.files[0])
                  }
                  className="w-full"
                />
              </div>
              <button
                type="button"
                onClick={() => deleteCandidate(index)}
                className="absolute top-2 right-2 px-3 py-1 text-red-500 text-sm rounded focus:outline-none focus:ring-2 focus:ring-red-300"
              >
                remove
              </button>
            </div>
          ))}

          <button
            type="submit"
            disabled={candidates.length === 0}
            className="w-full px-4 py-2 bg-green-500 text-white font-semibold rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-300"
          >
            Create Poll
          </button>
        </form>
      )}
    </div>
  );
}

export default PollForm;

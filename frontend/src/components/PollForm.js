import { useState } from "react";
import { toast } from "react-toastify";
function PollForm() {
  const [pollName, setPollName] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [candidates, setCandidates] = useState([]);

  // Handler to add a new candidate
  const addCandidate = () => {
    setCandidates([...candidates, { name: "", details: "", portfolio: null }]);
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

    const formData = new FormData();
    formData.append("pollName", pollName);
    formData.append("startDate", startDate);
    formData.append("endDate", endDate);
    candidates.forEach((candidate, index) => {
      formData.append(`candidates[${index}][name]`, candidate.name);
      formData.append(`candidates[${index}][details]`, candidate.details);
      if (candidate.portfolio) {
        formData.append(`candidates[${index}][portfolio]`, candidate.portfolio);
      }
    });

    try {
      const response = await fetch(
        "http://election.zapto.org/admin/updatePoll",
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
    } catch (error) {
      console.error("Error creating poll:", error);
    }
  };

  return (
    <div>
      <form
        onSubmit={handleSubmit}
        className="max-w-2xl mx-auto bg-gray-100 p-8 shadow-md rounded-md"
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

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-gray-800 font-medium mb-1">
              Start Date:
            </label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>
          <div>
            <label className="block text-gray-800 font-medium mb-1">
              End Date:
            </label>
            <input
              type="date"
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
            className="border border-gray-300 rounded-lg p-4 mb-4 bg-white"
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
                Details:
              </label>
              <textarea
                value={candidate.details}
                onChange={(e) =>
                  handleCandidateChange(index, "details", e.target.value)
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
          </div>
        ))}

        <button
          type="submit"
          className="w-full px-4 py-2 bg-green-500 text-white font-semibold rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-300"
        >
          Create Poll
        </button>
      </form>
    </div>
  );
}

export default PollForm;

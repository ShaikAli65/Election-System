import { useEffect, useState } from "react";
import data from "../utils/sampleCandidates";
import CandidateForm from "./CandidateForm";
const AddCandidates = () => {
  const [candidatesList, setCandidatesList] = useState([]);
  const [showForm, setShowForm] = useState(false);
  useEffect(() => {
    fetchCandidates();
  }, []);
  const fetchCandidates = async () => {
    const data = await fetch("http://election.zapto.org/admin/getCandidates");
    const json_data = await data.json();

    setCandidatesList(json_data);
  };
  const handleClick = () => {
    setShowForm(true);
  };
  return (
    <div>
      <h1>Candidates List</h1>
      <br></br>
      <button className="bg-black text-white rounded" onClick={handleClick}>
        Add Candidate
      </button>
      {showForm == true ? (
        <CandidateForm setShowForm={() => setShowForm(false)} />
      ) : (
        <></>
      )}

      {candidatesList.map((candidate) => (
        <div className="border-4 mb-2">
          <h1>Name: {candidate.name}</h1>
          <h1>Email: {candidate.email}</h1>
          <h1>Age: {candidate.age}</h1>
          <h1>Gender: {candidate.gender}</h1>
        </div>
      ))}
    </div>
  );
};
export default AddCandidates;

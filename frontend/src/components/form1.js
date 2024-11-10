const CandidateForm = ({ setShowForm }) => {
  const handleClick = () => {
    setShowForm();
  };
  return (
    <div>
      <form>
        <label>Name: </label>
        <input className="border border-gray-300 rounded-md p-2"></input>
        <br></br>
        <br></br>
        <label>Age: </label>
        <input className="border border-gray-300 rounded-md p-2"></input>
        <br></br>
        <button onClick={handleClick} className="bg-black text-white">
          Submit
        </button>
      </form>
    </div>
  );
};

export default CandidateForm;

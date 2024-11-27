const DisplayCandidate = ({ data, onAddItem }) => {
  const handleAdd = () => {
    const newItem = data;

    onAddItem(newItem);
  };
  return (
    <div className="px-4 m-2 border border-gray-300  flex justify-between">
      <div>
        <h1>{data.name} </h1>
      </div>
      <div>
        <button
          className="bg-black text-white rounded-lg px-4 py-2 m-2"
          onClick={handleAdd}
        >
          Add Candidate
        </button>
      </div>
    </div>
  );
};
export default DisplayCandidate;

import { useNavigate } from "react-router-dom";
const Admin = () => {
  const navigate = useNavigate();
  const handleClick = () => {
    navigate("/admin/createPoll");
  };
  return (
    <div>
      <h1>Admin Dashboard</h1>
      <div>
        <button className="bg-black text-white" onClick={handleClick}>
          Create Poll
        </button>
      </div>
    </div>
  );
};
export default Admin;

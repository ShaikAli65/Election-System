import DisplayPoll from "./DisplayPoll";
import { useState, useEffect } from "react";
const Polls = () => {
  const [data, setData] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://election.zapto.org/admin/getPolls"
        ); // Replace with your API endpoint
        if (!response.ok) {
          throw new Error("Failed to fetch poll data");
        }
        const result = await response.json();
        setData(result); // Update state with fetched data
        console.log(result);
      } catch (error) {
        console.log(error.message); // Set error if fetch fails
      }
    };

    fetchData();
  }, []);
  /*
      <div className="polls-list">
      
    </div>
      */
  return (
    <div>
      {data.map((poll) => (
        <DisplayPoll data={poll} key={poll.election_id} />
      ))}
    </div>
  );
};
export default Polls;

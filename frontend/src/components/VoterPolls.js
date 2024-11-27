import DisplayPoll from "./DisplayPoll";
import { useState, useEffect } from "react";
import { useUser } from "../contexts/UserContext";
import DisplayPollVoter from "./DisplayPollVoter";
const VoterPolls = () => {
  const [data, setData] = useState([]);
  const { user, setUser } = useUser();
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://election.zapto.org/voter/getPolls",
          {
            method: "GET", // You can omit this if GET is the default method
            headers: {
              "Content-Type": "application/json",
              access_token: user[1],
            },
          }
        ); // Replace with your API endpoint
        console.log(user);

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
        <DisplayPollVoter data={poll} key={poll.election_id} />
      ))}
    </div>
  );
};
export default VoterPolls;

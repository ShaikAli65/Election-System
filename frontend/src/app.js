import React from "react";
import ReactDOM from "react-dom";
import { Outlet, createBrowserRouter, RouterProvider } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Header from "./components/Header";
import Body from "./components/Body";
import Polls from "./components/Polls";
import Admin from "./components/Admin";
import CreatePoll from "./components/CreatePoll";
import AddCandidates from "./components/AddCandidates";
import UserLogin from "./components/UserLogin";
import VotesBarChart from "./components/VotesBarChart";
import PollForm from "./components/PollFOrm";
import RecaptchaTrial from "./components/RecaptchaTrial";
import DisplayPollComplete from "./components/DisplayPollComplete";
import { UserContextProvider } from "./contexts/UserContext";
import DisplayPollCompleteVoter from "./components/DisplayPollCompleteVoter";
import VoterPolls from "./components/VoterPolls";
const AppLayout = () => {
  return (
    <div className="app">
      <Header />
      <ToastContainer position="top-center" autoClose={3000} />
      <Outlet />
    </div>
  );
};
const appRouter = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      {
        path: "/",
        element: <Body />,
      },
      {
        path: "/voter/polls",
        element: <VoterPolls />,
      },
      {
        path: "/admin",
        element: <Admin />,
      },
      {
        path: "/admin/createPoll",
        element: <CreatePoll />,
      },
      {
        path: "/admin/addCandidates",
        element: <AddCandidates />,
      },
      {
        path: "/voter/login",
        element: <UserLogin />,
      },
      {
        path: "/bar",
        element: <VotesBarChart />,
      },
      {
        path: "/a",
        element: <PollForm />,
      },
      {
        path: "/admin/polls",
        element: <Polls />,
      },
      {
        path: "/test",
        element: <RecaptchaTrial />,
      },
      {
        path: "/admin/polls/:poll_id",
        element: <DisplayPollComplete />,
      },
      {
        path: "/voter/poll/:poll_id",
        element: <DisplayPollCompleteVoter />,
      },
    ],
  },
]);
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <UserContextProvider>
    <RouterProvider router={appRouter} />
  </UserContextProvider>
);

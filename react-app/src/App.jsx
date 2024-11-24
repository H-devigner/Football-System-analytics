import React, { useEffect, useState } from "react";
import {
   fetchCompetitions,
   fetchTeams,
   fetchPlayers,
   fetchMatches,
} from "./api";

const Dashboard = () => {
   const [competitions, setCompetitions] = useState([]);
   const [teams, setTeams] = useState([]);
   const [players, setPlayers] = useState([]);
   const [matches, setMatches] = useState([]);

   useEffect(() => {
       const loadData = async () => {
           const competitionsData = await fetchCompetitions();
           const teamsData = await fetchTeams();
           const playersData = await fetchPlayers();
           const matchesData = await fetchMatches();

           setCompetitions(competitionsData.data);
           setTeams(teamsData.data);
           setPlayers(playersData.data);
           setMatches(matchesData.data);
       };

       loadData();
   }, []);

   return (
       <div className="dashboard">
           <h1>Football Analytics Dashboard</h1>

           <section>
               <h2>Competitions</h2>
               <ul>
                   {competitions.map((competition) => (
                       <li key={competition.id}>{competition.name}</li>
                   ))}
               </ul>
           </section>

           <section>
               <h2>Teams</h2>
               <ul>
                   {teams.map((team) => (
                       <li key={team.id}>{team.name}</li>
                   ))}
               </ul>
           </section>

           <section>
               <h2>Players</h2>
               <ul>
                   {players.map((player) => (
                       <li key={player.id}>{player.name}</li>
                   ))}
               </ul>
           </section>

           <section>
               <h2>Matches</h2>
               <ul>
                   {matches.map((match) => (
                       <li key={match.id}>
                           {match.home_team.name} vs {match.away_team.name}
                       </li>
                   ))}
               </ul>
           </section>
       </div>
   );
};

export default Dashboard;

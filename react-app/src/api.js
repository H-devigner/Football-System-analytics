import axios from "axios";

const API_URL = "http://localhost:8001"; // Replace with your backend URL

export const fetchCompetitions = () => axios.get(`${API_URL}/competitions/`);
export const fetchTeams = () => axios.get(`${API_URL}/teams/`);
export const fetchPlayers = () => axios.get(`${API_URL}/players/`);
export const fetchMatches = () => axios.get(`${API_URL}/matches/`);
export const fetchMatchStatistics = () =>
    axios.get(`${API_URL}/match-statistics/`);
export const fetchSeasonTeamPerformances = () =>
    axios.get(`${API_URL}/season-team-performances/`);
export const fetchPlayerStatistics = () =>
    axios.get(`${API_URL}/player-statistics/`);
export const fetchSeasonPlayerStats = () =>
    axios.get(`${API_URL}/season-player-stats/`);
export const fetchTeamFormGuide = () => axios.get(`${API_URL}/team-form-guide/`);
export const fetchHeadToHead = () => axios.get(`${API_URL}/head-to-head/`);

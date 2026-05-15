"use client";

import React, { useState } from "react";
import { Search, Users, Zap, Shield, Filter, MoreHorizontal } from "lucide-react";
import { motion } from "framer-motion";

const CandidateCard = ({ name, role, location, skills, match }: any) => (
  <motion.div 
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="glass p-6 rounded-xl hover:shadow-[0_0_20px_rgba(59,130,246,0.1)] transition-all group"
  >
    <div className="flex justify-between items-start mb-4">
      <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-xl font-bold">
        {name[0]}
      </div>
      <div className="flex items-center gap-2">
        <span className="text-xs font-medium px-2 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
          {match}% Match
        </span>
        <button className="text-zinc-500 hover:text-white transition-colors">
          <MoreHorizontal size={18} />
        </button>
      </div>
    </div>
    
    <h3 className="text-lg font-semibold mb-1 group-hover:text-blue-400 transition-colors">{name}</h3>
    <p className="text-sm text-zinc-400 mb-4">{role} • {location}</p>
    
    <div className="flex flex-wrap gap-2 mb-4">
      {skills.map((skill: string) => (
        <span key={skill} className="text-[10px] uppercase tracking-wider font-bold px-2 py-0.5 rounded bg-zinc-800 text-zinc-300">
          {skill}
        </span>
      ))}
    </div>
    
    <button className="w-full py-2 bg-zinc-800 hover:bg-blue-600 text-white rounded-lg text-sm font-medium transition-all">
      View Profile
    </button>
  </motion.div>
);

export default function Dashboard() {
  const [query, setQuery] = useState("");
  
  const mockCandidates = [
    { name: "Alex Rivers", role: "Senior Golang Engineer", location: "Remote", skills: ["Go", "Kafka", "Postgres"], match: 98 },
    { name: "Sarah Chen", role: "Full Stack Developer", location: "Bengaluru", skills: ["React", "Node.js", "TypeScript"], match: 94 },
    { name: "Marcus Thorne", role: "DevOps Architect", location: "London", skills: ["AWS", "Kubernetes", "Terraform"], match: 89 },
    { name: "Elena Rodriguez", role: "Frontend Lead", location: "Madrid", skills: ["Next.js", "Tailwind", "Framer"], match: 92 },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      <header className="mb-12 flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-bold mb-2 tracking-tight">
            Recruiter <span className="gradient-text">Intelligence</span>
          </h1>
          <p className="text-zinc-400">Autonomous talent extraction and ranking engine.</p>
        </div>
        <div className="flex gap-3">
          <div className="glass px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium">
            <Zap size={16} className="text-yellow-500" />
            <span>Agent Active</span>
          </div>
        </div>
      </header>

      <div className="relative mb-12">
        <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
          <Search size={20} className="text-zinc-500" />
        </div>
        <input 
          type="text" 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Describe your ideal candidate (e.g., 'Senior Go engineer with Kafka experience in Bengaluru')"
          className="w-full bg-zinc-900/50 border border-zinc-800 focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/10 rounded-2xl py-4 pl-12 pr-4 outline-none transition-all text-lg"
        />
        <div className="absolute right-3 inset-y-2">
          <button className="h-full px-6 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-semibold transition-all flex items-center gap-2 shadow-lg shadow-blue-500/20">
            Start Search
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        <div className="glass p-6 rounded-2xl flex flex-col gap-1">
          <span className="text-zinc-500 text-sm font-medium flex items-center gap-2">
            <Users size={14} /> Total Sourced
          </span>
          <span className="text-3xl font-bold">1,284</span>
        </div>
        <div className="glass p-6 rounded-2xl flex flex-col gap-1">
          <span className="text-zinc-500 text-sm font-medium flex items-center gap-2">
            <Zap size={14} /> AI Screened
          </span>
          <span className="text-3xl font-bold">842</span>
        </div>
        <div className="glass p-6 rounded-2xl flex flex-col gap-1">
          <span className="text-zinc-500 text-sm font-medium flex items-center gap-2">
            <Shield size={14} /> Verified
          </span>
          <span className="text-3xl font-bold">126</span>
        </div>
        <div className="glass p-6 rounded-2xl flex flex-col gap-1">
          <span className="text-zinc-500 text-sm font-medium flex items-center gap-2">
            <Filter size={14} /> Active Jobs
          </span>
          <span className="text-3xl font-bold">12</span>
        </div>
      </div>

      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">Top Matches</h2>
        <div className="flex gap-2 text-sm font-medium text-zinc-400">
          <span>Sort by:</span>
          <select className="bg-transparent border-none outline-none text-white cursor-pointer">
            <option>Relevance</option>
            <option>Recency</option>
            <option>Match %</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {mockCandidates.map((c) => (
          <CandidateCard key={c.name} {...c} />
        ))}
      </div>
    </div>
  );
}

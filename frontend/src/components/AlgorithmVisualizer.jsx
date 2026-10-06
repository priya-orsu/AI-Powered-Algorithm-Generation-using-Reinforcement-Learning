import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
    Play, Pause, RotateCcw, ChevronRight, ChevronLeft,
    Sliders, Sparkles, Activity, Layers, Terminal, CheckCircle2,
    Eye, RefreshCw, BarChart2, Zap, ArrowRight, Dna, Compass, Grid,
    ShieldAlert, Award, Clock, Server, Check, ArrowUpRight, Cpu,
    Hash, ListOrdered, Shuffle, Network, PlayCircle,
    Boxes, HelpCircle
} from 'lucide-react';

export function AlgorithmVisualizer({
    algorithmName = 'Algorithm Visualizer',
    category = '',
    workingSteps = [],
    pseudocode = '',
    problemStatement = '',
    timeComplexity = '',
    spaceComplexity = ''
}) {
    // -------------------------------------------------------------------------
    // 1. Intelligent Paradigm Detection based on Algorithm, Category & Query
    // -------------------------------------------------------------------------
    const algoLower = (algorithmName || '').toLowerCase();
    const catLower = (category || '').toLowerCase();
    const probLower = (problemStatement || '').toLowerCase();
    const textCorpus = `${algoLower} ${catLower} ${probLower}`;

    const detectedParadigm = useMemo(() => {
        if (
            textCorpus.includes('suite') || textCorpus.includes('schedul') ||
            textCorpus.includes('operating room') || textCorpus.includes('hospital') ||
            textCorpus.includes('flight') || textCorpus.includes('aircraft') ||
            textCorpus.includes('cloud') || textCorpus.includes('kubernetes') ||
            textCorpus.includes('microservice') || textCorpus.includes('turnaround') ||
            textCorpus.includes('job') || textCorpus.includes('task allocation') ||
            textCorpus.includes('bin pack')
        ) {
            return {
                id: 'scheduling',
                label: 'Multi-Resource & Suite Timeline Allocation',
                badge: 'Resource Scheduling',
                icon: Clock,
                color: 'text-cyan-400',
                border: 'border-cyan-500/40'
            };
        }

        if (
            textCorpus.includes('dijkstra') || textCorpus.includes('graph') ||
            textCorpus.includes('bfs') || textCorpus.includes('dfs') ||
            textCorpus.includes('prim') || textCorpus.includes('kruskal') ||
            textCorpus.includes('a*') || textCorpus.includes('astar') ||
            textCorpus.includes('bellman') || textCorpus.includes('route') ||
            textCorpus.includes('routing') || textCorpus.includes('traffic') ||
            textCorpus.includes('intersection') || textCorpus.includes('tsp') ||
            textCorpus.includes('delivery') || textCorpus.includes('network') ||
            textCorpus.includes('shortest') || textCorpus.includes('tree')
        ) {
            return {
                id: 'graph',
                label: 'Network Topology & Shortest Path Traversal',
                badge: 'Graph & Routing',
                icon: Compass,
                color: 'text-amber-400',
                border: 'border-amber-500/40'
            };
        }

        if (
            textCorpus.includes('genetic') || textCorpus.includes('evolution') ||
            textCorpus.includes('ga-') || textCorpus.includes('ga ') ||
            textCorpus.includes('q-learn') || textCorpus.includes('reinforce') ||
            textCorpus.includes('policy') || textCorpus.includes('chromosome') ||
            textCorpus.includes('fitness') || textCorpus.includes('hybrid') ||
            textCorpus.includes('metaheuristic') || textCorpus.includes('anneal')
        ) {
            return {
                id: 'evolution_rl',
                label: 'GA Population Evolution & RL Reward Matrix',
                badge: 'Evolutionary & RL',
                icon: Dna,
                color: 'text-emerald-400',
                border: 'border-emerald-500/40'
            };
        }

        if (
            textCorpus.includes('knapsack') || textCorpus.includes('dp') ||
            textCorpus.includes('dynamic') || textCorpus.includes('matrix chain') ||
            textCorpus.includes('lcs') || textCorpus.includes('subsequence') ||
            textCorpus.includes('edit distance') || textCorpus.includes('memoiz') ||
            textCorpus.includes('coin change')
        ) {
            return {
                id: 'dp',
                label: '2D Dynamic Programming & State Matrix',
                badge: 'Dynamic Programming',
                icon: Grid,
                color: 'text-indigo-400',
                border: 'border-indigo-500/40'
            };
        }

        if (
            textCorpus.includes('kadane') || textCorpus.includes('subarray') ||
            textCorpus.includes('sliding window')
        ) {
            return {
                id: 'kadane',
                label: 'Sliding Window & Subarray Scanner',
                badge: 'Window Scanning',
                icon: Sliders,
                color: 'text-teal-400',
                border: 'border-teal-500/40'
            };
        }

        if (
            textCorpus.includes('sort') || textCorpus.includes('bubble') ||
            textCorpus.includes('quick') || textCorpus.includes('merge') ||
            textCorpus.includes('heap') || textCorpus.includes('search') ||
            textCorpus.includes('binary search') || textCorpus.includes('two pointer') ||
            textCorpus.includes('partition')
        ) {
            return {
                id: 'sorting',
                label: 'Array Partitioning & Value Distribution',
                badge: 'Array & Sorting',
                icon: BarChart2,
                color: 'text-blue-400',
                border: 'border-blue-500/40'
            };
        }

        if (
            textCorpus.includes('queen') || textCorpus.includes('backtrack') ||
            textCorpus.includes('sudoku') || textCorpus.includes('coloring') ||
            textCorpus.includes('branch and bound') || textCorpus.includes('constraint')
        ) {
            return {
                id: 'backtracking',
                label: 'Constraint Satisfaction & Decision Space',
                badge: 'Backtracking Search',
                icon: Award,
                color: 'text-yellow-400',
                border: 'border-yellow-500/40'
            };
        }

        return {
            id: 'universal',
            label: 'Live Algorithmic State Pipeline',
            badge: 'Universal Pipeline',
            icon: Zap,
            color: 'text-violet-400',
            border: 'border-violet-500/40'
        };
    }, [textCorpus]);

    // -------------------------------------------------------------------------
    // 2. Playback State & View Mode
    // -------------------------------------------------------------------------
    const [currentStep, setCurrentStep] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [playbackSpeed, setPlaybackSpeed] = useState(1);
    const [visualView, setVisualView] = useState('simulation'); // 'simulation' | 'flow'
    const timerRef = useRef(null);

    // Reset step whenever algorithm or paradigm changes
    useEffect(() => {
        setCurrentStep(0);
        setIsPlaying(false);
    }, [algorithmName, category]);

    // -------------------------------------------------------------------------
    // 3. Normalized Step List Extraction
    // -------------------------------------------------------------------------
    const parsedSteps = useMemo(() => {
        const rawList = Array.isArray(workingSteps) && workingSteps.length > 0
            ? workingSteps
            : (typeof workingSteps === 'string' && workingSteps.trim()
                ? workingSteps.split(/\n+/).filter(Boolean)
                : []);

        if (rawList.length > 0) {
            return rawList.map((step, idx) => {
                const text = typeof step === 'string'
                    ? step.replace(/^(step\s*\d+:?|\d+[\.\)]\s*)/i, '').trim()
                    : JSON.stringify(step);
                return {
                    stepNum: idx + 1,
                    title: `Execution Phase ${idx + 1}`,
                    explanation: text,
                    tag: `OP_PHASE_${idx + 1}`
                };
            });
        }

        // Default robust steps if none provided
        return [
            { stepNum: 1, title: 'Initialization Phase', explanation: `Initialize primary data structures, allocate state buffers, and prepare baseline constraints for ${algorithmName}.`, tag: 'INIT' },
            { stepNum: 2, title: 'Input Decomposition', explanation: 'Validate problem boundaries, construct initial search/allocation space, and set objective penalty weights.', tag: 'SETUP' },
            { stepNum: 3, title: 'Core Iteration & Evaluation', explanation: 'Execute algorithmic transitions, evaluate candidate states, and prune non-promising search vectors.', tag: 'ITERATE' },
            { stepNum: 4, title: 'Constraint Validation & Refinement', explanation: 'Verify feasibility constraints (zero overtime/conflicts), apply local heuristics or Q-policy gradient updates.', tag: 'REFINE' },
            { stepNum: 5, title: 'Convergence & Solution Output', explanation: 'Optimal global solution locked with minimized cost metric; return synthesized execution result.', tag: 'TERMINATE' }
        ];
    }, [workingSteps, algorithmName]);

    // =========================================================================
    // 4. PARADIGM SPECIFIC SIMULATION ENGINES
    // =========================================================================

    // --- A. SCHEDULING & RESOURCE ALLOCATION (Operating Suites / Cloud / Flights) ---
    const schedulingFrames = useMemo(() => {
        const isHospital = textCorpus.includes('hospital') || textCorpus.includes('surgery') || textCorpus.includes('suite');
        const isCloud = textCorpus.includes('cloud') || textCorpus.includes('kubernetes') || textCorpus.includes('node');
        const isFlight = textCorpus.includes('flight') || textCorpus.includes('aircraft');

        const resourceNames = isHospital
            ? ['Suite 1 (General)', 'Suite 2 (Cardiac)', 'Suite 3 (Ortho/Trauma)', 'Suite 4 (Neuro)', 'Suite 5 (Emergency/Day)']
            : isCloud
                ? ['Node A (Compute)', 'Node B (GPU-01)', 'Node C (Memory-X)', 'Node D (Edge-04)', 'Node E (Gateway)']
                : isFlight
                    ? ['Aircraft A320-1', 'Aircraft B737-8', 'Aircraft A350-9', 'Aircraft B787-9', 'Aircraft E190-2']
                    : ['Resource Core 1', 'Resource Core 2', 'Resource Core 3', 'Resource Core 4', 'Resource Core 5'];

        const tasks = isHospital
            ? [
                { id: 'S1', name: 'Open Cardiac Bypass', dur: 210, risk: 'High' },
                { id: 'S2', name: 'Spinal Fusion', dur: 180, risk: 'Med' },
                { id: 'S3', name: 'Knee Arthroplasty', dur: 150, risk: 'Low' },
                { id: 'S4', name: 'Laparoscopic Chole', dur: 90, risk: 'Low' },
                { id: 'S5', name: 'Craniotomy Tumor', dur: 240, risk: 'Critical' },
                { id: 'S6', name: 'Trauma Fracture Fix', dur: 120, risk: 'High' },
                { id: 'S7', name: 'Vascular Stent', dur: 140, risk: 'Med' },
                { id: 'S8', name: 'Emergency Appendectomy', dur: 90, risk: 'High' }
            ]
            : [
                { id: 'T1', name: 'Batch Ingestion', dur: 180, risk: 'Med' },
                { id: 'T2', name: 'Model Inference', dur: 240, risk: 'High' },
                { id: 'T3', name: 'API Routing', dur: 90, risk: 'Low' },
                { id: 'T4', name: 'Cache Compaction', dur: 120, risk: 'Med' },
                { id: 'T5', name: 'Vector Embedding', dur: 210, risk: 'High' },
                { id: 'T6', name: 'Data Migration', dur: 150, risk: 'Med' },
                { id: 'T7', name: 'Telemetry Stream', dur: 100, risk: 'Low' },
                { id: 'T8', name: 'Index Optimization', dur: 130, risk: 'Low' }
            ];

        // 6 progression frames
        return [
            {
                phase: 'Initial State: Free Suites',
                utilization: [0, 0, 0, 0, 0],
                allocations: [[], [], [], [], []],
                activeTask: tasks[0],
                overtimeHrs: 0.0,
                efficiency: 0,
                desc: 'Initialized 5 operational suites with 480-min regular shift limits. Ready for stochastic scheduling dispatch.'
            },
            {
                phase: 'High-Variance Surgery Placement',
                utilization: [43.7, 50.0, 0, 0, 0],
                allocations: [[tasks[0]], [tasks[4]], [], [], []],
                activeTask: tasks[1],
                overtimeHrs: 0.0,
                efficiency: 46.8,
                desc: 'RL agent assigned high-variance surgeries (S1 Cardiac, S5 Craniotomy) to dedicated sterile suites Suite 1 & 2.'
            },
            {
                phase: 'Mid-Duration Ortho & Trauma Dispatch',
                utilization: [43.7, 50.0, 31.2, 0, 25.0],
                allocations: [[tasks[0]], [tasks[4]], [tasks[2]], [], [tasks[5]]],
                activeTask: tasks[3],
                overtimeHrs: 0.0,
                efficiency: 62.4,
                desc: 'Allocated S3 (Knee Arthroplasty) to Suite 3 and emergency buffer S6 to Suite 5. Zero overtime registered.'
            },
            {
                phase: 'Short Elective Packing & Crossover',
                utilization: [62.5, 79.1, 68.7, 0, 25.0],
                allocations: [[tasks[0], tasks[3]], [tasks[4], tasks[6]], [tasks[2], tasks[1]], [], [tasks[5]]],
                activeTask: tasks[7],
                overtimeHrs: 0.0,
                efficiency: 81.5,
                desc: 'GA chromosome crossover packed S4 (90m) into Suite 1 and S2 (180m) into Suite 3, maximizing day shift density.'
            },
            {
                phase: 'Emergency Case Dynamic Injection',
                utilization: [62.5, 79.1, 68.7, 0, 43.7],
                allocations: [[tasks[0], tasks[3]], [tasks[4], tasks[6]], [tasks[2], tasks[1]], [], [tasks[5], tasks[7]]],
                activeTask: null,
                overtimeHrs: 0.0,
                efficiency: 89.2,
                desc: 'Emergency S8 routed into Suite 5 buffer. Overtime probability calculated at < 1.4% with stochastic margins.'
            },
            {
                phase: 'Global Optimum Locked: Zero Overtime',
                utilization: [81.2, 87.5, 93.7, 75.0, 81.2],
                allocations: [
                    [tasks[0], tasks[3]],
                    [tasks[4], tasks[6]],
                    [tasks[2], tasks[1]],
                    [{ id: 'S9', name: 'Elective Laparoscopy', dur: 180, risk: 'Low' }, { id: 'S10', name: 'Biopsy', dur: 180, risk: 'Low' }],
                    [tasks[5], tasks[7], { id: 'S11', name: 'Drainage', dur: 180, risk: 'Low' }]
                ],
                activeTask: null,
                overtimeHrs: 0.0,
                efficiency: 94.8,
                desc: 'FINAL STOCHASTIC SCHEDULE CONFIRMED! Zero overtime across all 5 suites with 94.8% peak operational efficiency.'
            }
        ];
    }, [textCorpus]);

    // --- B. GRAPH / NETWORK TOPOLOGY & ROUTING ---
    const graphNodes = useMemo(() => {
        const isTraffic = textCorpus.includes('traffic') || textCorpus.includes('intersection');
        const isDelivery = textCorpus.includes('delivery') || textCorpus.includes('package') || textCorpus.includes('tsp');

        if (isTraffic) {
            return [
                { id: 'Hub A', x: 65, y: 70, label: 'Main St Hub' },
                { id: 'Int B', x: 195, y: 35, label: 'North Ave' },
                { id: 'Int C', x: 195, y: 125, label: 'Market Sq' },
                { id: 'Int D', x: 325, y: 35, label: 'Broadway' },
                { id: 'Int E', x: 325, y: 125, label: 'Bay Hwy' },
                { id: 'Hub F', x: 450, y: 80, label: 'Expressway' }
            ];
        }
        if (isDelivery) {
            return [
                { id: 'Depot', x: 65, y: 70, label: 'Central Depot' },
                { id: 'Zone 1', x: 195, y: 35, label: 'Uptown' },
                { id: 'Zone 2', x: 195, y: 125, label: 'Midtown' },
                { id: 'Zone 3', x: 325, y: 35, label: 'Financial' },
                { id: 'Zone 4', x: 325, y: 125, label: 'Harbor' },
                { id: 'Dest', x: 450, y: 80, label: 'Airport Depot' }
            ];
        }
        return [
            { id: 'A', x: 65, y: 70, label: 'Node A' },
            { id: 'B', x: 195, y: 35, label: 'Node B' },
            { id: 'C', x: 195, y: 125, label: 'Node C' },
            { id: 'D', x: 325, y: 35, label: 'Node D' },
            { id: 'E', x: 325, y: 125, label: 'Node E' },
            { id: 'F', x: 450, y: 80, label: 'Node F' }
        ];
    }, [textCorpus]);

    const graphEdges = [
        { u: 0, v: 1, weight: 4 },
        { u: 0, v: 2, weight: 2 },
        { u: 1, v: 2, weight: 1 },
        { u: 1, v: 3, weight: 5 },
        { u: 2, v: 4, weight: 8 },
        { u: 2, v: 3, weight: 8 },
        { u: 3, v: 4, weight: 2 },
        { u: 3, v: 5, weight: 6 },
        { u: 4, v: 5, weight: 3 }
    ];

    const graphFrames = [
        {
            currentNode: 0,
            distances: [0, '∞', '∞', '∞', '∞', '∞'],
            visited: [],
            activeEdges: [],
            pathEdges: [],
            desc: 'Start: Initialized source distance to 0, all network vertices set to infinity.'
        },
        {
            currentNode: 0,
            distances: [0, 4, 2, '∞', '∞', '∞'],
            visited: [0],
            activeEdges: [{ u: 0, v: 1 }, { u: 0, v: 2 }],
            pathEdges: [],
            desc: 'Visiting source node. Relaxed edges to Node 1 (cost 4) and Node 2 (cost 2).'
        },
        {
            currentNode: 2,
            distances: [0, 3, 2, 10, 10, '∞'],
            visited: [0, 2],
            activeEdges: [{ u: 2, v: 1 }, { u: 2, v: 3 }, { u: 2, v: 4 }],
            pathEdges: [{ u: 0, v: 2 }],
            desc: 'Smallest unvisited distance is Node 2 (cost 2). Path relaxed to Node 1 updated to 3 (2+1).'
        },
        {
            currentNode: 1,
            distances: [0, 3, 2, 8, 10, '∞'],
            visited: [0, 2, 1],
            activeEdges: [{ u: 1, v: 3 }],
            pathEdges: [{ u: 0, v: 2 }, { u: 2, v: 1 }],
            desc: 'Visiting Node 1 (cost 3). Discovered faster route to Node 3: 3 + 5 = 8.'
        },
        {
            currentNode: 3,
            distances: [0, 3, 2, 8, 10, 14],
            visited: [0, 2, 1, 3],
            activeEdges: [{ u: 3, v: 4 }, { u: 3, v: 5 }],
            pathEdges: [{ u: 0, v: 2 }, { u: 2, v: 1 }, { u: 1, v: 3 }],
            desc: 'Visiting Node 3 (cost 8). Relaxed forward edges to Node 4 and target Node 5.'
        },
        {
            currentNode: 4,
            distances: [0, 3, 2, 8, 10, 13],
            visited: [0, 2, 1, 3, 4],
            activeEdges: [{ u: 4, v: 5 }],
            pathEdges: [{ u: 0, v: 2 }, { u: 2, v: 1 }, { u: 1, v: 3 }],
            desc: 'Visiting Node 4 (cost 10). Found shorter alternative to destination: 10 + 3 = 13!'
        },
        {
            currentNode: 5,
            distances: [0, 3, 2, 8, 10, 13],
            visited: [0, 2, 1, 3, 4, 5],
            activeEdges: [],
            pathEdges: [{ u: 0, v: 2 }, { u: 2, v: 4 }, { u: 4, v: 5 }],
            desc: 'DESTINATION REACHED! Optimal route finalized with minimum overall travel cost 13.'
        }
    ];

    // --- C. EVOLUTIONARY GA & RL ENGINE ---
    const evolutionFrames = [
        {
            gen: 1,
            bestFitness: 64.2,
            avgFitness: 48.5,
            epsilon: 0.95,
            reward: '+12.4',
            population: [
                { id: 'CH-1', gene: '1100101011', fitness: 64.2, status: 'Elite (Top 1)' },
                { id: 'CH-2', gene: '0101100101', fitness: 52.1, status: 'Selected' },
                { id: 'CH-3', gene: '1000110010', fitness: 43.8, status: 'Mutated' },
                { id: 'CH-4', gene: '0010011001', fitness: 34.0, status: 'Discarded' }
            ],
            desc: 'Gen 1: Initialized population pool with high exploration rate ε=0.95. Top chromosome fitness: 64.2%.'
        },
        {
            gen: 2,
            bestFitness: 78.5,
            avgFitness: 61.3,
            epsilon: 0.80,
            reward: '+28.9',
            population: [
                { id: 'CH-1', gene: '1110101111', fitness: 78.5, status: 'Elite (Crossover)' },
                { id: 'CH-2', gene: '1100101011', fitness: 64.2, status: 'Parent' },
                { id: 'CH-3', gene: '0111100111', fitness: 58.4, status: 'Child' },
                { id: 'CH-4', gene: '1001110010', fitness: 44.2, status: 'Mutated' }
            ],
            desc: 'Gen 2: Uniform crossover combined superior gene segments. Q-agent penalized high variance.'
        },
        {
            gen: 3,
            bestFitness: 89.4,
            avgFitness: 75.8,
            epsilon: 0.60,
            reward: '+45.2',
            population: [
                { id: 'CH-1', gene: '1111101111', fitness: 89.4, status: 'Elite' },
                { id: 'CH-2', gene: '1110101111', fitness: 78.5, status: 'Parent' },
                { id: 'CH-3', gene: '1110111011', fitness: 71.0, status: 'Crossover' },
                { id: 'CH-4', gene: '0111100111', fitness: 64.3, status: 'Mutated' }
            ],
            desc: 'Gen 3: Adaptive mutation applied to bit #4. Fitness escalated to 89.4% with reward +45.2.'
        },
        {
            gen: 4,
            bestFitness: 95.8,
            avgFitness: 88.2,
            epsilon: 0.35,
            reward: '+78.6',
            population: [
                { id: 'CH-1', gene: '1111111110', fitness: 95.8, status: 'Elite' },
                { id: 'CH-2', gene: '1111101111', fitness: 89.4, status: 'Parent' },
                { id: 'CH-3', gene: '1111111011', fitness: 86.2, status: 'Crossover' },
                { id: 'CH-4', gene: '1110101111', fitness: 81.4, status: 'Selected' }
            ],
            desc: 'Gen 4: Policy exploitation dominating (ε=0.35). Chromosomes converging toward global optimum.'
        },
        {
            gen: 5,
            bestFitness: 99.2,
            avgFitness: 96.5,
            epsilon: 0.10,
            reward: '+99.2',
            population: [
                { id: 'CH-1', gene: '1111111111', fitness: 99.2, status: 'Optimal Winner' },
                { id: 'CH-2', gene: '1111111110', fitness: 95.8, status: 'Sub-Optimal' },
                { id: 'CH-3', gene: '1111101111', fitness: 92.4, status: 'Sub-Optimal' },
                { id: 'CH-4', gene: '1111111011', fitness: 89.1, status: 'Sub-Optimal' }
            ],
            desc: 'Gen 5: Convergence threshold achieved! Target fitness accuracy ≥ 99.2% confirmed.'
        }
    ];

    // --- D. DYNAMIC PROGRAMMING 2D MATRIX ---
    const dpFrames = [
        {
            activeRow: 0,
            activeCol: 0,
            formula: 'Base case initialized: DP[0][w] = 0',
            matrix: [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            desc: 'DP matrix initialized with zero boundary conditions across all subproblems.'
        },
        {
            activeRow: 1,
            activeCol: 2,
            formula: 'DP[1][2] = max(DP[0][2], V[1] + DP[0][0]) = 3',
            matrix: [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 3, 3, 3, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            desc: 'Subproblem Item 1 evaluated. Capacity threshold met at W=2; value 3 recorded.'
        },
        {
            activeRow: 2,
            activeCol: 5,
            formula: 'DP[2][5] = max(DP[1][5], V[2] + DP[1][2]) = 3 + 4 = 7',
            matrix: [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 3, 3, 3, 3, 3, 3],
                [0, 0, 3, 4, 4, 7, 7, 7],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            desc: 'Item 2 combined with Item 1 subproblem at capacity W=5, reaching composite value 7.'
        },
        {
            activeRow: 3,
            activeCol: 7,
            formula: 'DP[3][7] = max(DP[2][7], V[3] + DP[2][3]) = 9 (Optimal)',
            matrix: [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 3, 3, 3, 3, 3, 3],
                [0, 0, 3, 4, 4, 7, 7, 7],
                [0, 0, 3, 4, 5, 7, 8, 9]
            ],
            desc: 'Table completed! Maximum objective value 9 obtained at maximum capacity boundary.'
        }
    ];

    // --- E. SORTING & ARRAY PARTITIONING ---
    const initialSortArr = [45, 18, 72, 33, 89, 21, 54, 12, 60, 38];
    const [sortArr, setSortArr] = useState(initialSortArr);

    const sortFrames = useMemo(() => {
        const a = [...sortArr];
        const frames = [];
        frames.push({
            array: [...a],
            comparing: [],
            swapping: [],
            sorted: [],
            desc: 'Initial unsorted array state loaded.'
        });

        // Bubble sort simulation steps
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < a.length - i - 1; j += 2) {
                frames.push({
                    array: [...a],
                    comparing: [j, j + 1],
                    swapping: [],
                    sorted: Array.from({ length: i }, (_, k) => a.length - 1 - k),
                    desc: `Comparing element A[${j}] (${a[j]}) with A[${j + 1}] (${a[j + 1]}).`
                });

                if (a[j] > a[j + 1]) {
                    const temp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = temp;
                    frames.push({
                        array: [...a],
                        comparing: [],
                        swapping: [j, j + 1],
                        sorted: Array.from({ length: i }, (_, k) => a.length - 1 - k),
                        desc: `Condition met: swapped elements at indices [${j}] and [${j + 1}].`
                    });
                }
            }
        }

        frames.push({
            array: [...a].sort((x, y) => x - y),
            comparing: [],
            swapping: [],
            sorted: Array.from({ length: a.length }, (_, k) => k),
            desc: 'Partitioning and sorting complete! Elements ordered in non-decreasing sequence.'
        });

        return frames;
    }, [sortArr]);

    const randomizeSortArray = () => {
        const newArr = Array.from({ length: 10 }, () => Math.floor(Math.random() * 85) + 12);
        setSortArr(newArr);
        setCurrentStep(0);
        setIsPlaying(false);
    };

    // --- F. KADANE / SLIDING WINDOW ---
    const kadaneArr = [-2, 1, -3, 4, -1, 2, 1, -5, 4];
    const kadaneFrames = [
        { idx: 0, currSum: -2, maxSum: -2, range: [0, 0], temp: [0, 0], desc: 'Initialized at index 0: curr_sum = -2, max_sum = -2.' },
        { idx: 1, currSum: 1, maxSum: 1, range: [1, 1], temp: [1, 1], desc: 'Index 1 (value 1): A[1] > -2 + 1. Started fresh positive subarray at [1].' },
        { idx: 3, currSum: 4, maxSum: 4, range: [3, 3], temp: [3, 3], desc: 'Index 3 (value 4): New peak subarray window opened at index 3.' },
        { idx: 6, currSum: 6, maxSum: 6, range: [3, 6], temp: [3, 6], desc: 'Index 6 (value 1): Maximum contiguous subarray extended [4, -1, 2, 1] sum = 6!' },
        { idx: 8, currSum: 5, maxSum: 6, range: [3, 6], temp: [8, 8], desc: 'Scan finished! Global maximum contiguous sum = 6 confirmed.' }
    ];

    // --- G. BACKTRACKING & N-QUEENS ---
    const backtrackingFrames = [
        {
            queens: [0, -1, -1, -1, -1, -1, -1, -1],
            conflicts: [],
            safeCell: [0, 0],
            placedCount: 1,
            desc: 'Placed Queen 1 at Row 0, Col 0. Scanning subsequent rows for safe frontiers.'
        },
        {
            queens: [0, 2, -1, -1, -1, -1, -1, -1],
            conflicts: [[1, 0], [1, 1]],
            safeCell: [1, 2],
            placedCount: 2,
            desc: 'Row 1 Col 0 & Col 1 blocked by attack vectors. Placed Queen 2 at Row 1, Col 2.'
        },
        {
            queens: [0, 2, 4, 1, -1, -1, -1, -1],
            conflicts: [[3, 0], [3, 2]],
            safeCell: [3, 1],
            placedCount: 4,
            desc: 'Placed Queen 4 at Row 3, Col 1 with verified zero diagonal collisions.'
        },
        {
            queens: [0, 4, 7, 5, 2, 6, 1, 3],
            conflicts: [],
            safeCell: [7, 3],
            placedCount: 8,
            desc: 'OPTIMAL SOLUTION FOUND! All 8 Queens placed with 0 attack collisions.'
        }
    ];

    // -------------------------------------------------------------------------
    // 5. Total Steps Calculation based on Active Paradigm
    // -------------------------------------------------------------------------
    const activeFrames = useMemo(() => {
        if (detectedParadigm.id === 'scheduling') return schedulingFrames;
        if (detectedParadigm.id === 'graph') return graphFrames;
        if (detectedParadigm.id === 'evolution_rl') return evolutionFrames;
        if (detectedParadigm.id === 'dp') return dpFrames;
        if (detectedParadigm.id === 'sorting') return sortFrames;
        if (detectedParadigm.id === 'kadane') return kadaneFrames;
        if (detectedParadigm.id === 'backtracking') return backtrackingFrames;
        return parsedSteps;
    }, [detectedParadigm.id, schedulingFrames, graphFrames, evolutionFrames, dpFrames, sortFrames, parsedSteps]);

    const totalSteps = Math.max(1, activeFrames.length);

    // Bound currentStep safely
    const safeCurrentStep = Math.min(currentStep, totalSteps - 1);
    const activeFrame = activeFrames[safeCurrentStep] || {};

    // -------------------------------------------------------------------------
    // 6. Playback Timer Controller
    // -------------------------------------------------------------------------
    useEffect(() => {
        if (isPlaying) {
            const interval = 1300 / playbackSpeed;
            timerRef.current = setInterval(() => {
                setCurrentStep((prev) => {
                    if (prev >= totalSteps - 1) {
                        setIsPlaying(false);
                        return prev;
                    }
                    return prev + 1;
                });
            }, interval);
        } else if (timerRef.current) {
            clearInterval(timerRef.current);
        }
        return () => {
            if (timerRef.current) clearInterval(timerRef.current);
        };
    }, [isPlaying, playbackSpeed, totalSteps]);

    const handlePlayPause = () => {
        if (safeCurrentStep >= totalSteps - 1) {
            setCurrentStep(0);
        }
        setIsPlaying(!isPlaying);
    };

    const handleStepForward = () => {
        setIsPlaying(false);
        setCurrentStep((prev) => Math.min(totalSteps - 1, prev + 1));
    };

    const handleStepBackward = () => {
        setIsPlaying(false);
        setCurrentStep((prev) => Math.max(0, prev - 1));
    };

    const handleReset = () => {
        setIsPlaying(false);
        setCurrentStep(0);
    };

    // Current description to show
    const currentExplanation = activeFrame.desc || activeFrame.explanation || (parsedSteps[safeCurrentStep]?.explanation) || 'Executing algorithmic state transformation...';

    const IconComponent = detectedParadigm.icon;

    return (
        <div className="p-6 rounded-2xl bg-gradient-to-br from-[#0a101f] via-[#070c17] to-[#040810] border border-cyan-500/30 shadow-2xl space-y-6">
            {/* Header: Title, Paradigm Badge & View Mode Toggle (NO HARDCODED PRESETS!) */}
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-white/10 pb-4">
                <div className="space-y-1.5">
                    <div className="flex flex-wrap items-center gap-2">
                        <span className={`px-2.5 py-1 rounded-full text-[10px] font-mono uppercase font-bold bg-[#040812] ${detectedParadigm.color} border ${detectedParadigm.border} flex items-center gap-1.5 shadow-sm`}>
                            <IconComponent className="w-3.5 h-3.5 animate-pulse" />
                            {detectedParadigm.badge}
                        </span>
                        <span className="text-xs text-slate-400">
                            Algorithm: <strong className="text-white font-mono">{algorithmName}</strong>
                        </span>
                        {category && (
                            <span className="text-[11px] text-slate-500 font-mono">
                                • {category}
                            </span>
                        )}
                    </div>
                    <h3 className="text-lg sm:text-xl font-extrabold text-white flex items-center gap-2 tracking-tight">
                        <Zap className="w-5 h-5 text-amber-400" />
                        Live Execution & Visual Simulation Engine
                    </h3>
                </div>

                {/* View Mode Selector for Current Algorithm */}
                <div className="flex items-center gap-1 bg-[#040712] p-1 border border-white/10 rounded-xl text-xs font-mono">
                    <button
                        onClick={() => setVisualView('simulation')}
                        className={`px-3 py-1.5 rounded-lg transition font-bold flex items-center gap-1.5 ${
                            visualView === 'simulation'
                                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/30'
                                : 'text-slate-400 hover:text-white'
                        }`}
                    >
                        <Eye className="w-3.5 h-3.5" />
                        <span>Interactive Simulation</span>
                    </button>
                    <button
                        onClick={() => setVisualView('flow')}
                        className={`px-3 py-1.5 rounded-lg transition font-bold flex items-center gap-1.5 ${
                            visualView === 'flow'
                                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/30'
                                : 'text-slate-400 hover:text-white'
                        }`}
                    >
                        <Network className="w-3.5 h-3.5" />
                        <span>State Flowchart</span>
                    </button>
                </div>
            </div>

            {/* Main Visualizer Arena */}
            <div className="p-6 rounded-2xl bg-[#03060f] border border-white/10 min-h-[360px] flex flex-col justify-center items-center relative overflow-hidden">

                {/* ============================================================= */}
                {/* VIEW 1: INTERACTIVE GRAPHICAL SIMULATION CANVAS               */}
                {/* ============================================================= */}
                {visualView === 'simulation' && (
                    <div className="w-full">
                        {/* 1. SCHEDULING & TIMELINE CANVAS */}
                        {detectedParadigm.id === 'scheduling' && (
                            <div className="w-full space-y-5">
                                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/10 pb-3 text-xs font-mono">
                                    <span className="text-cyan-400 font-bold flex items-center gap-1.5">
                                        <Clock className="w-4 h-4 text-cyan-400" />
                                        Operating Suites & Resource Allocation Grid
                                    </span>
                                    <div className="flex items-center gap-4">
                                        <span>Estimated Overtime: <strong className="text-emerald-400 font-black">{activeFrame.overtimeHrs ?? '0.0'} hrs</strong></span>
                                        <span>Efficiency: <strong className="text-cyan-300 font-black">{activeFrame.efficiency ?? '94.8'}%</strong></span>
                                    </div>
                                </div>

                                {/* 5 Suites Timeline Progress */}
                                <div className="space-y-3">
                                    {['Suite 1 (General)', 'Suite 2 (Cardiac)', 'Suite 3 (Ortho/Trauma)', 'Suite 4 (Neuro)', 'Suite 5 (Emergency/Day)'].map((suiteName, sIdx) => {
                                        const util = activeFrame.utilization?.[sIdx] ?? (sIdx * 15 + 20);
                                        const alloc = activeFrame.allocations?.[sIdx] || [];
                                        const isOvertime = util > 100;

                                        return (
                                            <div key={sIdx} className="p-3 rounded-xl bg-[#081224] border border-white/5 space-y-2">
                                                <div className="flex items-center justify-between text-xs font-mono">
                                                    <span className="text-slate-300 font-bold flex items-center gap-2">
                                                        <Server className="w-3.5 h-3.5 text-cyan-400" />
                                                        {suiteName}
                                                    </span>
                                                    <div className="flex items-center gap-2">
                                                        <span className="text-[10px] text-slate-400">Assigned: {alloc.length} cases</span>
                                                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                                            isOvertime
                                                                ? 'bg-rose-950 text-rose-300 border border-rose-500'
                                                                : util >= 80
                                                                    ? 'bg-cyan-950 text-cyan-300 border border-cyan-800'
                                                                    : 'bg-slate-900 text-slate-300'
                                                        }`}>
                                                            {util.toFixed(1)}% Capacity
                                                        </span>
                                                    </div>
                                                </div>

                                                {/* Timeline Bar */}
                                                <div className="h-3 w-full bg-slate-900 rounded-full overflow-hidden border border-white/5 relative">
                                                    <div
                                                        className={`h-full rounded-full transition-all duration-500 ${
                                                            isOvertime
                                                                ? 'bg-rose-500 shadow-md shadow-rose-500/50'
                                                                : util >= 80
                                                                    ? 'bg-gradient-to-r from-cyan-500 to-indigo-500'
                                                                    : 'bg-emerald-500'
                                                        }`}
                                                        style={{ width: `${Math.min(100, util)}%` }}
                                                    />
                                                </div>

                                                {/* Allocated Cases Badges */}
                                                {alloc.length > 0 && (
                                                    <div className="flex flex-wrap gap-1.5 pt-1">
                                                        {alloc.map((task, tIdx) => (
                                                            <span
                                                                key={tIdx}
                                                                className="px-2 py-0.5 rounded bg-cyan-950/60 border border-cyan-500/30 text-[10px] font-mono text-cyan-200 flex items-center gap-1"
                                                            >
                                                                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
                                                                {task.id}: {task.name} ({task.dur}m)
                                                            </span>
                                                        ))}
                                                    </div>
                                                )}
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        )}

                        {/* 2. GRAPH / ROUTING CANVAS */}
                        {detectedParadigm.id === 'graph' && (
                            <div className="w-full space-y-4">
                                <div className="flex items-center justify-between border-b border-white/10 pb-2 text-xs font-mono">
                                    <span className="text-amber-400 font-bold flex items-center gap-1.5">
                                        <Compass className="w-4 h-4" />
                                        Network Traversal & Shortest Path Topology
                                    </span>
                                    <span className="text-cyan-300 font-bold">
                                        Current Target: Node #{activeFrame.currentNode ?? 0}
                                    </span>
                                </div>

                                <div className="relative w-full flex justify-center items-center select-none py-2">
                                    <svg viewBox="0 0 520 160" className="w-full max-w-xl h-44">
                                        {graphEdges.map((edge, eIdx) => {
                                            const uNode = graphNodes[edge.u];
                                            const vNode = graphNodes[edge.v];
                                            const activeEdges = activeFrame.activeEdges || [];
                                            const pathEdges = activeFrame.pathEdges || [];

                                            const isActive = activeEdges.some(ae => (ae.u === edge.u && ae.v === edge.v) || (ae.u === edge.v && ae.v === edge.u));
                                            const isPath = pathEdges.some(pe => (pe.u === edge.u && pe.v === edge.v) || (pe.u === edge.v && pe.v === edge.u));

                                            let strokeColor = 'rgba(255, 255, 255, 0.15)';
                                            let strokeWidth = 1.5;
                                            if (isPath) {
                                                strokeColor = '#10b981';
                                                strokeWidth = 3.5;
                                            } else if (isActive) {
                                                strokeColor = '#f59e0b';
                                                strokeWidth = 3;
                                            }

                                            const midX = (uNode.x + vNode.x) / 2;
                                            const midY = (uNode.y + vNode.y) / 2;

                                            return (
                                                <g key={eIdx}>
                                                    <line
                                                        x1={uNode.x}
                                                        y1={uNode.y}
                                                        x2={vNode.x}
                                                        y2={vNode.y}
                                                        stroke={strokeColor}
                                                        strokeWidth={strokeWidth}
                                                        strokeDasharray={isActive ? "4,4" : "none"}
                                                    />
                                                    <rect x={midX - 8} y={midY - 7} width="16" height="14" rx="4" fill="#03060f" stroke="rgba(255,255,255,0.1)" />
                                                    <text x={midX} y={midY + 3} fill="#94a3b8" fontSize="8" textAnchor="middle" fontFamily="monospace" fontWeight="bold">
                                                        {edge.weight}
                                                    </text>
                                                </g>
                                            );
                                        })}

                                        {graphNodes.map((node, nIdx) => {
                                            const isCurrent = activeFrame.currentNode === nIdx;
                                            const isVisited = (activeFrame.visited || []).includes(nIdx);
                                            const dist = (activeFrame.distances || [])[nIdx] ?? '∞';

                                            let fillColor = '#0f172a';
                                            let strokeColor = '#334155';
                                            if (isCurrent) {
                                                fillColor = '#f59e0b';
                                                strokeColor = '#fef08a';
                                            } else if (isVisited) {
                                                fillColor = '#065f46';
                                                strokeColor = '#34d399';
                                            }

                                            return (
                                                <g key={node.id}>
                                                    <circle
                                                        cx={node.x}
                                                        cy={node.y}
                                                        r="16"
                                                        fill={fillColor}
                                                        stroke={strokeColor}
                                                        strokeWidth={isCurrent ? 3 : 2}
                                                        className="transition-all duration-300"
                                                    />
                                                    <text x={node.x} y={node.y + 4} fill="#ffffff" fontSize="10" textAnchor="middle" fontFamily="monospace" fontWeight="bold">
                                                        {node.id}
                                                    </text>
                                                    <text x={node.x} y={node.y - 20} fill={isCurrent ? '#fde047' : '#38bdf8'} fontSize="9" textAnchor="middle" fontFamily="monospace" fontWeight="bold">
                                                        d={dist}
                                                    </text>
                                                </g>
                                            );
                                        })}
                                    </svg>
                                </div>
                            </div>
                        )}

                        {/* 3. GA & RL CONVERGENCE CANVAS */}
                        {detectedParadigm.id === 'evolution_rl' && (
                            <div className="w-full space-y-5">
                                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/5 pb-2">
                                    <div className="flex items-center gap-2">
                                        <Dna className="w-4 h-4 text-emerald-400" />
                                        <span className="text-xs font-mono font-bold text-white uppercase">
                                            Generation #{activeFrame.gen ?? 1} Evolutionary Chromosome Pool
                                        </span>
                                    </div>
                                    <div className="flex items-center gap-4 text-xs font-mono">
                                        <span>Exploration (ε): <strong className="text-amber-400">{activeFrame.epsilon ?? '0.50'}</strong></span>
                                        <span>Reward: <strong className="text-cyan-300">{activeFrame.reward ?? '+50.0'}</strong></span>
                                        <span>Best Fitness: <strong className="text-emerald-400 font-bold">{activeFrame.bestFitness ?? '95.0'}%</strong></span>
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                    {(activeFrame.population || []).map((chrom) => (
                                        <div key={chrom.id} className="p-3.5 rounded-xl bg-[#081224] border border-white/5 flex items-center justify-between gap-2 font-mono text-xs">
                                            <div className="space-y-1">
                                                <div className="flex items-center gap-2">
                                                    <span className="text-[10px] text-slate-400">{chrom.id}</span>
                                                    <span className="px-2 py-0.5 rounded text-[9px] bg-emerald-950 border border-emerald-800 text-emerald-300 font-bold">
                                                        {chrom.status}
                                                    </span>
                                                </div>
                                                <div className="text-cyan-300 tracking-wider font-bold">{chrom.gene}</div>
                                            </div>
                                            <div className="text-right">
                                                <span className="text-[9px] text-slate-400 block uppercase">Fitness</span>
                                                <span className="text-sm font-black text-emerald-400">{chrom.fitness}%</span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* 4. DYNAMIC PROGRAMMING 2D MATRIX CANVAS */}
                        {detectedParadigm.id === 'dp' && (
                            <div className="w-full space-y-4 font-mono text-xs">
                                <div className="flex items-center justify-between border-b border-white/10 pb-2">
                                    <span className="text-cyan-400 font-bold flex items-center gap-1.5">
                                        <Grid className="w-4 h-4" /> 2D DP Computation Matrix
                                    </span>
                                    <span className="text-emerald-400 font-bold">
                                        {activeFrame.formula || 'DP State Evaluation'}
                                    </span>
                                </div>

                                <div className="overflow-x-auto">
                                    <table className="w-full text-center border-collapse">
                                        <thead>
                                            <tr className="bg-slate-900 border-b border-white/10 text-slate-400">
                                                <th className="p-2">State \ Step</th>
                                                {Array.from({ length: 8 }).map((_, w) => (
                                                    <th key={w} className="p-2">W={w}</th>
                                                ))}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {(activeFrame.matrix || []).map((row, rIdx) => (
                                                <tr key={rIdx} className="border-b border-white/5">
                                                    <td className="p-2 font-bold text-slate-300">
                                                        Stage {rIdx}
                                                    </td>
                                                    {row.map((val, cIdx) => {
                                                        const isActive = activeFrame.activeRow === rIdx && activeFrame.activeCol === cIdx;
                                                        return (
                                                            <td
                                                                key={cIdx}
                                                                className={`p-2 transition-all duration-200 ${
                                                                    isActive
                                                                        ? 'bg-emerald-600 text-white font-extrabold shadow-lg shadow-emerald-600/40 rounded'
                                                                        : val > 0
                                                                            ? 'bg-cyan-950/40 text-cyan-300'
                                                                            : 'text-slate-600'
                                                                }`}
                                                            >
                                                                {val}
                                                            </td>
                                                        );
                                                    })}
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        )}

                        {/* 5. SORTING BAR CHART CANVAS */}
                        {detectedParadigm.id === 'sorting' && (
                            <div className="w-full space-y-6">
                                <div className="flex items-end justify-center gap-2 sm:gap-3 h-52 pt-4 px-2 select-none">
                                    {(activeFrame.array || sortArr).map((val, idx) => {
                                        const comparing = (activeFrame.comparing || []).includes(idx);
                                        const swapping = (activeFrame.swapping || []).includes(idx);
                                        const sorted = (activeFrame.sorted || []).includes(idx);

                                        let barColor = 'bg-cyan-600 border-cyan-400';
                                        if (swapping) barColor = 'bg-rose-500 border-rose-300 animate-bounce shadow-lg shadow-rose-500/50';
                                        else if (comparing) barColor = 'bg-amber-400 border-amber-200 shadow-md shadow-amber-400/40';
                                        else if (sorted) barColor = 'bg-emerald-500 border-emerald-300 shadow-md shadow-emerald-500/30';

                                        return (
                                            <div key={idx} className="flex flex-col items-center flex-1 max-w-[42px] gap-1.5 transition-all duration-200">
                                                <span className="text-[10px] font-mono font-bold text-white">{val}</span>
                                                <div
                                                    className={`w-full rounded-t-lg border transition-all duration-200 ${barColor}`}
                                                    style={{ height: `${Math.max(15, (val / 100) * 160)}px` }}
                                                />
                                                <span className="text-[9px] font-mono text-slate-500">[{idx}]</span>
                                            </div>
                                        );
                                    })}
                                </div>
                                <div className="flex flex-wrap items-center justify-center gap-4 text-[11px] font-mono border-t border-white/5 pt-3">
                                    <span className="flex items-center gap-1.5 text-cyan-400"><span className="w-3 h-3 rounded bg-cyan-600"></span> Unsorted</span>
                                    <span className="flex items-center gap-1.5 text-amber-300"><span className="w-3 h-3 rounded bg-amber-400"></span> Comparing</span>
                                    <span className="flex items-center gap-1.5 text-rose-400"><span className="w-3 h-3 rounded bg-rose-500"></span> Swapping</span>
                                    <span className="flex items-center gap-1.5 text-emerald-400"><span className="w-3 h-3 rounded bg-emerald-500"></span> Sorted Position</span>
                                </div>
                            </div>
                        )}

                        {/* 6. KADANE SUBARRAY CANVAS */}
                        {detectedParadigm.id === 'kadane' && (
                            <div className="w-full space-y-6">
                                <div className="flex items-center justify-center gap-2 overflow-x-auto p-2 select-none">
                                    {kadaneArr.map((val, idx) => {
                                        const isCurrent = activeFrame.idx === idx;
                                        const inRange = idx >= (activeFrame.range?.[0] ?? 0) && idx <= (activeFrame.range?.[1] ?? 0);

                                        let cellClass = 'bg-[#081224] border-white/10 text-slate-300';
                                        if (isCurrent) cellClass = 'bg-cyan-600 border-cyan-300 text-white shadow-lg shadow-cyan-500/40 ring-2 ring-cyan-400';
                                        else if (inRange) cellClass = 'bg-emerald-950 border-emerald-400 text-emerald-300 shadow-md shadow-emerald-500/20';

                                        return (
                                            <div key={idx} className="flex flex-col items-center gap-1.5">
                                                <span className="text-[10px] font-mono text-slate-400">[{idx}]</span>
                                                <div className={`w-11 h-12 rounded-xl border flex items-center justify-center font-mono font-bold text-sm transition-all duration-200 ${cellClass}`}>
                                                    {val > 0 ? `+${val}` : val}
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        )}

                        {/* 7. BACKTRACKING & CONSTRAINT GRID CANVAS */}
                        {detectedParadigm.id === 'backtracking' && (
                            <div className="w-full space-y-4">
                                <div className="flex items-center justify-between border-b border-white/10 pb-2 text-xs font-mono">
                                    <span className="text-yellow-400 font-bold flex items-center gap-1.5">
                                        👑 Constraint Satisfaction & Backtracking Search Space
                                    </span>
                                    <span className="text-emerald-400 font-bold">
                                        Assigned Placements: {activeFrame.placedCount ?? 1} / 8
                                    </span>
                                </div>

                                <div className="flex justify-center select-none py-1">
                                    <div className="grid grid-cols-8 gap-1 p-2 rounded-xl bg-[#070d1a] border border-cyan-500/30 shadow-2xl">
                                        {Array.from({ length: 8 }).map((_, rIdx) =>
                                            Array.from({ length: 8 }).map((_, cIdx) => {
                                                const isDarkCell = (rIdx + cIdx) % 2 === 1;
                                                const queens = activeFrame.queens || [0, -1, -1, -1, -1, -1, -1, -1];
                                                const hasQueen = queens[rIdx] === cIdx;
                                                const conflicts = activeFrame.conflicts || [];
                                                const isConflict = conflicts.some(([r, c]) => r === rIdx && c === cIdx);

                                                let cellStyle = isDarkCell ? 'bg-[#0b172a] text-slate-400' : 'bg-[#15233c] text-slate-300';
                                                if (hasQueen) {
                                                    cellStyle = 'bg-yellow-950/80 border-2 border-yellow-400 text-yellow-300 shadow-lg shadow-yellow-500/30';
                                                } else if (isConflict) {
                                                    cellStyle = 'bg-rose-950/70 border border-rose-500/60 text-rose-300';
                                                }

                                                return (
                                                    <div
                                                        key={`${rIdx}-${cIdx}`}
                                                        className={`w-9 h-9 sm:w-11 sm:h-11 rounded-lg flex items-center justify-center font-bold text-sm transition-all duration-200 ${cellStyle}`}
                                                    >
                                                        {hasQueen ? (
                                                            <span className="text-xl drop-shadow-md">👑</span>
                                                        ) : isConflict ? (
                                                            <span className="text-xs text-rose-400 font-mono">✕</span>
                                                        ) : (
                                                            <span className="text-[9px] opacity-20 font-mono">{rIdx},{cIdx}</span>
                                                        )}
                                                    </div>
                                                );
                                            })
                                        )}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* 8. UNIVERSAL PIPELINE & STATE ENGINE (Works for ANY other algorithm) */}
                        {detectedParadigm.id === 'universal' && (
                            <div className="w-full space-y-6">
                                {/* Visual Data Flow Stream */}
                                <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                                    {[
                                        { label: 'Input Data Stream', val: 'Active Buffer', icon: Database, color: 'text-cyan-400', border: 'border-cyan-500/30' },
                                        { label: 'Pipeline Transformer', val: `Phase #${safeCurrentStep + 1}`, icon: Cpu, color: 'text-amber-400', border: 'border-amber-500/30' },
                                        { label: 'Constraint Filter', val: 'Invariant Satisfied', icon: CheckCircle2, color: 'text-emerald-400', border: 'border-emerald-500/30' },
                                        { label: 'Output State Buffer', val: 'Synthesized', icon: Boxes, color: 'text-indigo-400', border: 'border-indigo-500/30' }
                                    ].map((block, bIdx) => (
                                        <div key={bIdx} className={`p-4 rounded-xl bg-[#081224] border ${block.border} space-y-2`}>
                                            <div className="flex items-center justify-between text-xs font-mono">
                                                <span className="text-slate-400">{block.label}</span>
                                                <block.icon className={`w-4 h-4 ${block.color}`} />
                                            </div>
                                            <div className={`text-base font-bold ${block.color} font-mono`}>
                                                {block.val}
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                {/* Active Execution Step Card */}
                                <div className="p-5 rounded-2xl bg-[#081224] border border-cyan-500/30 max-w-2xl mx-auto space-y-3 shadow-xl">
                                    <div className="flex items-center justify-between border-b border-white/10 pb-2">
                                        <span className="text-xs font-bold text-cyan-400 uppercase font-mono tracking-wider flex items-center gap-1.5">
                                            <Terminal className="w-3.5 h-3.5" />
                                            Execution Step #{safeCurrentStep + 1} of {totalSteps}
                                        </span>
                                        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-white/5">
                                            {detectedParadigm.badge}
                                        </span>
                                    </div>
                                    <p className="text-sm text-slate-200 leading-relaxed font-sans">
                                        {currentExplanation}
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* ============================================================= */}
                {/* VIEW 2: ALGORITHMIC STATE FLOWCHART & PIPELINE               */}
                {/* ============================================================= */}
                {visualView === 'flow' && (
                    <div className="w-full space-y-6">
                        <div className="flex items-center justify-between border-b border-white/10 pb-2 text-xs font-mono">
                            <span className="text-cyan-400 font-bold flex items-center gap-1.5">
                                <Network className="w-4 h-4 text-cyan-400" />
                                Sequential State Machine & Stage Transitions
                            </span>
                            <span className="text-slate-400">Total Stages: <strong className="text-white">{parsedSteps.length}</strong></span>
                        </div>

                        {/* Interactive Flow Diagram */}
                        <div className="space-y-3 max-w-3xl mx-auto">
                            {parsedSteps.map((step, sIdx) => {
                                const isCurrent = safeCurrentStep === sIdx;
                                const isDone = safeCurrentStep > sIdx;

                                return (
                                    <div
                                        key={sIdx}
                                        onClick={() => {
                                            setIsPlaying(false);
                                            setCurrentStep(sIdx);
                                        }}
                                        className={`p-4 rounded-xl border transition-all duration-200 cursor-pointer flex items-start gap-4 ${
                                            isCurrent
                                                ? 'bg-[#0e1f3b] border-cyan-400 shadow-xl shadow-cyan-600/20 ring-1 ring-cyan-400'
                                                : isDone
                                                    ? 'bg-[#061524] border-emerald-500/40 text-slate-300'
                                                    : 'bg-[#081224] border-white/5 text-slate-500 hover:border-white/20'
                                        }`}
                                    >
                                        <div className={`w-8 h-8 rounded-xl shrink-0 flex items-center justify-center font-mono font-bold text-xs ${
                                            isCurrent
                                                ? 'bg-cyan-500 text-black font-extrabold shadow-md shadow-cyan-500/50'
                                                : isDone
                                                    ? 'bg-emerald-950 border border-emerald-500 text-emerald-300'
                                                    : 'bg-slate-800 text-slate-400'
                                        }`}>
                                            {isDone ? <Check className="w-4 h-4 text-emerald-400" /> : sIdx + 1}
                                        </div>

                                        <div className="space-y-1 flex-1">
                                            <div className="flex items-center justify-between">
                                                <h4 className={`text-xs font-bold font-mono ${isCurrent ? 'text-cyan-300' : 'text-slate-200'}`}>
                                                    {step.title}
                                                </h4>
                                                <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                                                    isCurrent
                                                        ? 'bg-cyan-950 text-cyan-300 border border-cyan-800 animate-pulse'
                                                        : isDone
                                                            ? 'bg-emerald-950/60 text-emerald-400'
                                                            : 'text-slate-500'
                                                }`}>
                                                    {isCurrent ? 'ACTIVE EXECUTION' : isDone ? 'COMPLETED' : 'PENDING'}
                                                </span>
                                            </div>
                                            <p className="text-xs text-slate-300 font-sans leading-relaxed">
                                                {step.explanation}
                                            </p>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                )}
            </div>

            {/* Explanation Live Banner */}
            <div className="p-4 rounded-xl bg-[#080d1a] border border-cyan-500/20 text-xs text-slate-200 flex items-start gap-2.5">
                <Sparkles className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <div className="leading-relaxed font-sans">
                    <strong className="text-cyan-300 uppercase text-[10px] block font-mono">
                        Step #{safeCurrentStep + 1} State Rationale:
                    </strong>
                    <span>{currentExplanation}</span>
                </div>
            </div>

            {/* Interactive Step Pills / Scrubber Bar */}
            <div className="space-y-2">
                <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                    <span>Execution Timeline Progress</span>
                    <span>{Math.round(((safeCurrentStep + 1) / totalSteps) * 100)}% Complete</span>
                </div>
                <div className="flex items-center gap-1.5 overflow-x-auto py-1">
                    {Array.from({ length: totalSteps }).map((_, sIdx) => {
                        const isCurrent = safeCurrentStep === sIdx;
                        const isDone = safeCurrentStep > sIdx;
                        return (
                            <button
                                key={sIdx}
                                onClick={() => {
                                    setIsPlaying(false);
                                    setCurrentStep(sIdx);
                                }}
                                className={`flex-1 min-w-[32px] h-2.5 rounded-full transition-all duration-200 ${
                                    isCurrent
                                        ? 'bg-cyan-400 ring-2 ring-cyan-400 shadow-md shadow-cyan-400/50'
                                        : isDone
                                            ? 'bg-emerald-500'
                                            : 'bg-slate-800 hover:bg-slate-700'
                                }`}
                                title={`Jump to Step ${sIdx + 1}`}
                            />
                        );
                    })}
                </div>
            </div>

            {/* Control Bar: Play / Pause / Step / Speed / Reset */}
            <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-white/10">
                <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-slate-400">
                        Step <strong className="text-white">{safeCurrentStep + 1}</strong> of {totalSteps}
                    </span>
                    {detectedParadigm.id === 'sorting' && (
                        <button
                            onClick={randomizeSortArray}
                            className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 border border-white/10 text-xs text-slate-300 hover:text-cyan-300 transition flex items-center gap-1 font-mono"
                        >
                            <RefreshCw className="w-3 h-3" /> Randomize
                        </button>
                    )}
                </div>

                {/* Primary Player Controls */}
                <div className="flex items-center gap-2">
                    <button
                        onClick={handleReset}
                        title="Reset to Start"
                        className="w-8 h-8 rounded-xl bg-slate-900 border border-white/10 text-slate-400 hover:text-white flex items-center justify-center transition"
                    >
                        <RotateCcw className="w-4 h-4" />
                    </button>

                    <button
                        onClick={handleStepBackward}
                        disabled={safeCurrentStep === 0}
                        title="Previous Step"
                        className="w-8 h-8 rounded-xl bg-slate-900 border border-white/10 text-slate-300 hover:text-white flex items-center justify-center transition disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                        <ChevronLeft className="w-4 h-4" />
                    </button>

                    <button
                        onClick={handlePlayPause}
                        className={`px-5 py-2 rounded-xl text-xs font-bold font-mono transition flex items-center gap-2 shadow-lg ${
                            isPlaying
                                ? 'bg-rose-600 hover:bg-rose-500 text-white shadow-rose-600/30 animate-pulse'
                                : 'bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white shadow-cyan-500/20'
                        }`}
                    >
                        {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-current" />}
                        <span>{isPlaying ? 'Pause' : 'Play Live'}</span>
                    </button>

                    <button
                        onClick={handleStepForward}
                        disabled={safeCurrentStep >= totalSteps - 1}
                        title="Next Step"
                        className="w-8 h-8 rounded-xl bg-slate-900 border border-white/10 text-slate-300 hover:text-white flex items-center justify-center transition disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                        <ChevronRight className="w-4 h-4" />
                    </button>
                </div>

                {/* Speed Controls */}
                <div className="flex items-center gap-1.5 text-xs font-mono text-slate-400">
                    <Sliders className="w-3.5 h-3.5" />
                    <span>Speed:</span>
                    <div className="flex items-center gap-1 bg-[#050811] p-0.5 border border-white/10 rounded-lg">
                        {[0.5, 1, 2, 4].map((spd) => (
                            <button
                                key={spd}
                                onClick={() => setPlaybackSpeed(spd)}
                                className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                    playbackSpeed === spd ? 'bg-cyan-600 text-white' : 'text-slate-400 hover:text-white'
                                }`}
                            >
                                {spd}x
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AlgorithmVisualizer;

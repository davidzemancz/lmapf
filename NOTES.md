## 6.12.2025 Definice problému a postup řešení LMAPF
- Problém: lifelong MAPD
  - Kontinuálně přibývají úkoly (tasky) pro agenty, když dokončí sůvj aktuální
  - Úkol: cesta ke zboží a k výdejnímu místu
- Optimalizujeme: throughput = počet dosažených cílů za jednotku času
- Algoritmus [Algorithm 3 PIBT for MAPD](https://www.sciencedirect.com/science/article/pii/S0004370222000923?via%3Dihub))
  1. Přijmi nové úkoly a přidej do prioritní fronty
  2. Přiřaď nové úkoly volným agentům
  3. Rychle naplánuj cesty agentů s novým úkolem, volitelně uprav cesty stávajících agentů (od n kroků dále)

## 6.12.2025 MAPF řešení
- Umím spustit LaCam (zatím jen python implementaci) a vyřešit pomocí něj statickou MAPF úlohu
- Nyní nutno vyřešit pro lifelong MAPF:
  - Kdy spustit přepočet řešení?
    - Lze pomocí LaCam přepočítat jen část řešení? Cesty ostatních agentů jsou pohyblivé překážky.
    - Hodí se na to vůbec LaCam?
    - Prozatím použiji PIBT dle [článku](https://www.sciencedirect.com/science/article/pii/S0004370222000923?via%3Dihub)
  - Přiřazování cílů agentům -> task assigner
    - Heuristika dle vzdálenosti

## 24.11.2025 Zadání:
Automatic warehouses deploy hundreds or thousands of robots to fulfill customers' orders in a timely manner. Various multi-agent pathfinding (MAPF) algorithms were developed to navigate these agents in a collision-free manner while optimizing throughput. However, the placement of goods in the warehouse can significantly impact the effectiveness of MAPF algorithms by reducing congestion or shortening the travel distance for the most popular goods.

In this thesis, the student explores the impact of the placement of items of various popularity on the throughput of MAPF algorithms. Specifically, the student selects an effective MAPF algorithm and simulates an automatic warehouse where a stream of tasks is incoming. Assuming that each item has a different probability of being ordered, the student applies optimization techniques to determine the optimal storage location for each item within the warehouse.

## 18.11.2025 Užitečné odkazy
- [LaCAM](https://github.com/Kei18/pylacam)
- [LaCAM0](https://kei18.github.io/lacam2/)
- [Benchmarks](https://movingai.com/benchmarks/mapf.html)
- [MPAF](https://arxiv.org/pdf/1906.08291)
- [CPP PY binding](https://github.com/pybind/pybind11)

## 6.11.2025 Články
- [Scaling Lifelong Multi-Agent Path Finding to More Realistic Settings](https://arxiv.org/pdf/2404.16162)
- [Multi-Robot Coordination and Layout Design for Automated Warehousing](https://arxiv.org/pdf/2305.06436)
- [Enhancing Lifelong Multi-Agent Path Finding with Cache Mechanism](https://arxiv.org/html/2501.02803v1)
- [Priority inheritance with backtracking for iterative multi-agent path finding](https://www.sciencedirect.com/science/article/pii/S0004370222000923?via%3Dihub)
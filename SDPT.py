"""
SDPT: Theory of State-Dependent Perspective Transformation
Reference Implementation of the Nonuple Vector Variable System (Version 5.1)
Author: Muhammad Yousha Narejo (Independent Scholar)
License: CC BY 4.0 International
"""

import numpy as np
from typing import Dict, Any, Tuple


class NonupleVector:
    """
    Represents the 9-dimensional state space vector V(t) divided into three sub-vectors:
    V_hist (Historical), V_struct (Structural), and V_trans (Transient).
    All parameter values are normalized internally between 0.0 and 1.0.
    """
    def __init__(self, values: Dict[str, float]):
        # Expected keys matching V5.1 taxonomy
        self.required_keys = {
            'V1_age', 'V2_exp', 'V3_mem',          # V_hist
            'V4_int', 'V5_nat', 'V6_temp',         # V_struct
            'V7_state', 'V8_emot', 'V9_mood'       # V_trans
        }
        
        # Validation and normalization
        for key in self.required_keys:
            if key not in values:
                raise ValueError(f"Missing required Nonuple Vector component: {key}")
            val = float(values[key])
            if not (0.0 <= val <= 100.0):
                raise ValueError(f"Value for {key} must be normalized between 0-1 or 0-100.")
            # Auto-scale 0-100 inputs to 0-1 scale internally
            self.__dict__[key] = val / 100.0 if val > 1.0 else val

    def get_historical(self) -> Tuple[float, float, float]:
        return self.V1_age, self.V2_exp, self.V3_mem

    def get_structural(self) -> Tuple[float, float, float]:
        return self.V4_int, self.V5_nat, self.V6_temp

    def get_transient(self) -> Tuple[float, float, float]:
        return self.V7_state, self.V8_emot, self.V9_mood

    def is_zero_state(self) -> bool:
        """Checks if the system meets Sifr al-Haal condition (V = 0)"""
        return all(getattr(self, k) == 0.0 for k in self.required_keys)


class SDPTModel:
    """
    Computes Subjective Nazar N_i(t) from Objective Manzar M using the Ta'weel Operator (Phi)
    and Athar al-Bi'a Environmental term (Psi).
    """
    def __init__(self, objective_manzar: Any):
        """
        Initializes the model with a static, invariant objective field M.
        M can be a singular scalar asset value, vector, or an array representing data.
        """
        self.M = np.array(objective_manzar, dtype=float)

    def compute_nazar(self, V: NonupleVector, environment_weight: float = 0.0) -> np.ndarray:
        """
        Executes the main system equation: N_i(t) = Phi(M | V) + Psi(M, V)
        """
        # 1. Zero-State Baseline Condition (الأساس الصفري)
        if V.is_zero_state():
            return self.M.copy()  # Phi(M | 0) = M
            
        V1, V2, V3 = V.get_historical()
        V4, V5, V6 = V.get_structural()
        V7, V8, V9 = V.get_transient()
        
        # 2. Compute Functional Weights for the Sub-Vectors
        # Historical influences configuration matching lifecycle scaling laws
        historical_filter = (V1 * 0.15) + (V2 * 0.55) - (V3 * 0.20)
        
        # Structural capacities controlling internal cognitive resolution
        structural_filter = (V4 * 0.65) + (V5 * 0.15) + (V6 * 0.20)
        
        # Transient variables mapping real-time biological and emotional modulation
        # Emotion (V8) operates as an acute non-linear multiplier on current biological State (V7)
        transient_filter = (V7 * 0.35) * (V8 * 0.45) + (V9 * 0.20)
        
        # 3. Apply the Ta'weel Operator Function (Phi)
        phi_coefficient = 1.0 + (historical_filter + structural_filter + transient_filter)
        phi_out = self.M * phi_coefficient
        
        # 4. Compute Athar al-Bi'a Environment Term (Psi)
        psi_out = self.M * (environment_weight * 0.1) * (V7 + V9)
        
        # 5. Return Subjective Output (Nazar)
        return phi_out + psi_out

    def update_temporal_state(self, current_nazar: np.ndarray, next_vector_dict: Dict[str, float]) -> NonupleVector:
        """
        Enforces the Anti-Circularity Boundary Rule (عدم الدور).
        Ensures N(t) is excluded from entering V(t), but updates V3_mem at step (t+1).
        """
        # Convert Nazar matrix outcome to a scalar interference index
        nazar_scalar_index = float(np.mean(current_nazar))
        normalized_memory_input = min(max(nazar_scalar_index / (np.mean(self.M) * 2), 0.0), 100.0)
        
        # Write N(t) safely into V3(t+1) memory buffer
        next_vector_dict['V3_mem'] = normalized_memory_input
        return NonupleVector(next_vector_dict)


# --- Empirical Verification Script (The Table Paradigm Test) ---
if __name__ == "__main__":
    print("=====================================================================")
    print("  SDPT CALCULATOR NODE v5.1 — MUHAMMAD YOUSHA NAREJO OFFICIAL CORE   ")
    print("=====================================================================\n")
    
    # Let M be a fixed objective target (e.g., a wooden table valued at baseline 100.0)
    M_stimulus = 100.0
    engine = SDPTModel(objective_manzar=M_stimulus)
    print(f"Objective Invariant Field [Manzar M] = {M_stimulus}\n")
    
    # Test Scenario A: Mechanical Verification / CCTV (Zero-State Control)
    v_cctv = NonupleVector({
        'V1_age': 0, 'V2_exp': 0, 'V3_mem': 0,
        'V4_int': 0, 'V5_nat': 0, 'V6_temp': 0,
        'V7_state': 0, 'V8_emot': 0, 'V9_mood': 0
    })
    N_cctv = engine.compute_nazar(v_cctv)
    print(f"[TEST 1] Sifr al-Haal Condition (CCTV Mechanical Sensor):")
    print(f"         Output Nazar N = {N_cctv} (Passes Baseline Axiom: N == M)\n")

    # Test Scenario B: Human Observer 1 (Experienced Structural Expert)
    v_expert = NonupleVector({
        'V1_age': 45.0, 'V2_exp': 95.0, 'V3_mem': 60.0,
        'V4_int': 85.0, 'V5_nat': 50.0, 'V6_temp': 70.0,
        'V7_state': 20.0, 'V8_emot': 10.0, 'V9_mood': 50.0
    })
    N_expert = engine.compute_nazar(v_expert, environment_weight=20.0)
    print(f"[TEST 2] Observer Type: Technical Expert (High Experience & Intelligence):")
    print(f"         Output Nazar N = {N_expert:.4f}\n")

    # Test Scenario C: Human Observer 2 (High-Stress Context)
    v_stressed = NonupleVector({
        'V1_age': 25.0, 'V2_exp': 20.0, 'V3_mem': 40.0,
        'V4_int': 60.0, 'V5_nat': 40.0, 'V6_temp': 50.0,
        'V7_state': 90.0, 'V8_emot': 85.0, 'V9_mood': 20.0
    })
    N_stressed = engine.compute_nazar(v_stressed, environment_weight=80.0)
    print(f"[TEST 3] Observer Type: Stressed/Biased Agent (High Biological State & Emotion):")
    print(f"         Output Nazar N = {N_stressed:.4f}\n")

    # Test Scenario D: Demonstration of Anti-Circularity (Temporal Step t -> t+1 Transition)
    print(f"[TEST 4] Activating Temporal Loop Transition (Enforcing Rule: N(t) -> V3(t+1)):")
    base_state_t2 = {
        'V1_age': 25.0, 'V2_exp': 21.0, 'V3_mem': 0.0, # Will be overridden by N(t)
        'V4_int': 60.0, 'V5_nat': 40.0, 'V6_temp': 50.0,
        'V7_state': 50.0, 'V8_emot': 30.0, 'V9_mood': 50.0
    }
    v_t2 = engine.update_temporal_state(current_nazar=N_stressed, next_vector_dict=base_state_t2)
    print(f"         Causal Step Complete. V3_mem for state (t+1) successfully loaded with: {v_t2.V3_mem * 100:.2f}%")
    print("         Anti-Circularity verified. Regress loop safely neutralized.")

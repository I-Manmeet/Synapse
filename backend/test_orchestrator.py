from orchestrator import run_analysis


question = """
My clothing business sales decreased by 20%
over the last three months.

Analyze the business, identify the major risks,
and recommend a strategy to improve performance.
"""


result = run_analysis(question)


print("\n")
print("=" * 70)
print("FINAL SYNAPSE REPORT")
print("=" * 70)

print("\n")
print(result["final_report"])

print("\n")
print("=" * 70)
print("SYNAPSE ANALYSIS COMPLETED")
print("=" * 70)
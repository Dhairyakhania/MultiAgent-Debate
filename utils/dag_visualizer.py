def render_dag(app, output_path="dag.png"):
    try:
        app.get_graph().draw_png(output_path)
        print(f"[DAG] Graph saved to {output_path}")
    except Exception as e:
        print("[DAG] Graph rendering failed:", e)

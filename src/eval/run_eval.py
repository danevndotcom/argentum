from src.eval.tasks import (
    task_01_create_ping,
    task_02_create_nested_file,
    task_03_fix_stale_config,
    task_04_readonly_recovery,
)

TASKS = [
    task_01_create_ping.run_task,
    task_02_create_nested_file.run_task,
    task_03_fix_stale_config.run_task,
    task_04_readonly_recovery.run_task,
]

def main():
    print("=" * 60)
    print("ARGENTUM EVALUATION SUITE")
    print("=" * 60)
    passed = 0
    for task_fn in TASKS:
        res = task_fn()
        status = "PASS" if res.get("success") else "FAIL"
        print(f"[{status}] {res.get('task_id')}")
        if res.get("success"):
            passed += 1
    print("=" * 60)
    print(f"SUMMARY: {passed}/{len(TASKS)} tasks passed")
    print("=" * 60)

if __name__ == "__main__":
    main()

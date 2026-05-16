# Root Cause of Asyncio Loop Conflict

## The Issue
When executing the hiring workflow, an exception was raised stating:
```
It looks like you are using Playwright Sync API inside the asyncio loop.
Please use the Async API instead.
```

## Root Cause
The `run_hiring_workflow` was originally designed to run synchronously using `playwright.sync_api`. However, certain environments (such as FastAPI applications with `uvicorn`, Celery tasks that might implicitly create loops, or other async code) start an `asyncio` event loop. Playwright's `sync_playwright` explicitly checks if there is a running event loop (`asyncio.get_running_loop()`) and throws an exception if one exists, to prevent blocking the async loop with synchronous code.

When executing `python main.py` directly, an active asyncio loop was being inherited or created before Playwright was initialized, causing the synchronous API to crash immediately. By refactoring the entire browser automation and workflow orchestration layer to utilize `playwright.async_api`, the application can now run safely within asynchronous contexts like FastAPI backends, enabling scalable, concurrent multi-agent executions.

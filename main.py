from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, SessionLocal
from models.user import User
from my_routes import auth, jobs, applications

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Portal API",
    description="Backend API for Mini Job Portal App",
    version="1.0.0"
)


@app.on_event("startup")
def init_db():
    db = SessionLocal()
    try:
        existing_users = db.query(User).count()

        if existing_users == 0:
            recruiter = User(
                email="recruiter@test.com",
                password="123456",
                role="recruiter"
            )

            jobseeker = User(
                email="user@test.com",
                password="123456",
                role="jobseeker"
            )

            db.add(recruiter)
            db.add(jobseeker)
            db.commit()

            print("✓ Default users created successfully!")
            print("  - recruiter@test.com / 123456 (recruiter)")
            print("  - user@test.com / 123456 (jobseeker)")
        else:
            print("✓ Users already exist in database")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(applications.router)


@app.get("/")
def root():
    return {"message": "Job Portal API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

async def run_job_fsm(job_id: UUID):
    async with async_session() as db:
        job = await Job.get(db, job_id)
        if not job:
            return

        try:
            await job.update_status(db, JobStatus.PENDING)
            await job.update_state(db, JobState.EMBEDDING)
            image_bytes = await download_image(job.image_url)
            embedding = await embed_image(image_bytes)
            await job.update_state(db, JobState.INDEXING)
            await store_vector(job.id, embedding)

            await job.update_status(db, JobStatus.DONE)
            await job.update_state(db, JobState.COMPLETED)

        except Exception as e:
            await job.update_status(db, JobStatus.ERROR, detail=str(e))

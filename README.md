# quack
Quick Universal Automated Content Keeper is a project to help streamers label and categorize their content via transcripts.

QUACK leverages the YouTube API and AWS services to automatically download transcripts of your YouTube videos, store them in S3, and continuously check for new videos to process. The system can be deployed using AWS Lambda for serverless processing, with an emphasis on scalability, low cost, and ease of use.

Key Features:
- Automated Transcript Retrieval: Automatically download and store transcripts from YouTube videos.
- AWS S3 Storage: Securely store transcripts in an S3 bucket for easy access.
- Daily Updates: Automatically check for new videos and update transcripts daily.
- Serverless Architecture: Utilize AWS Lambda for efficient, scalable processing.

## Order of Operations
1) Create S3 bucket for storing transcripts and Lambda to embed via Titan on trigger for an upload to the bucket. This will then embed the transcript and store it in LanceDB in the same S3 Bucket.
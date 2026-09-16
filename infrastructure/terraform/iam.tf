resource "aws_iam_role" "filingpulse_task" {
  name = "filingpulse-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "filingpulse_raw_s3" {
  name = "filingpulse-raw-s3-access"
  role = aws_iam_role.filingpulse_task.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect   = "Allow"
        Action   = "s3:ListBucket"
        Resource = aws_s3_bucket.raw.arn
      }
    ]
  })
}
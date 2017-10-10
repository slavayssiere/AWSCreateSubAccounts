
jenkins_iam_assume_role = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::810499002773:user/Jenkins-iam",
          "arn:aws:iam::810499002773:user/TravisCIForIAMPolicies"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

jenkins_policy_role = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "cloudformation:*",
                "iam:*"
            ],
            "Resource": [
                "*"
            ],
            "Effect": "Allow"
        },
        {
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::amie01-s3-iam",
                "arn:aws:s3:::amie01-s3-iam/*"
            ],
            "Effect": "Allow"
        }
    ]
}
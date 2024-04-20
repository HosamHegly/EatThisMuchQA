pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                slackSend (color: '#00FF00', message: "Checkout stage completed successfully: ${env.JOB_NAME} [${env.BUILD_NUMBER}]")
            }
        }

        stage('Setup Docker Compose') {
            steps {
                script {
                    if (!fileExists('C:\\Program Files\\Docker\\docker-compose.exe')) {
                        bat 'curl -L "https://github.com/docker/compose/releases/download/v2.11.2/docker-compose-Windows-x86_64.exe" -o "C:\\Program Files\\Docker\\docker-compose.exe"'
                    }
                    slackSend (color: '#00FF00', message: "Setup Docker Compose completed: ${env.JOB_NAME} [${env.BUILD_NUMBER}]")
                }
            }
        }

        stage('Build  Docker Compose') {
            steps {
                script {
                    bat 'docker-compose build'
                }
                slackSend (color: '#FFFF00', message: "Build and run Docker Compose started: ${env.JOB_NAME} [${env.BUILD_NUMBER}]")
            }
        }

        stage('Test') {
            steps {
                script {
                    bat 'docker-compose build'
                    'docker-compose up -d'

                }
                slackSend (color: '#0000FF', message: "Testing completed: ${env.JOB_NAME} [${env.BUILD_NUMBER}]")
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    bat '"C:\\Program Files\\Docker\\docker-compose.exe" down'
                }
            }
            post {
                always {
                    slackSend (color: '#FF00FF', message: "Cleanup completed, build finished: ${env.JOB_NAME} [${env.BUILD_NUMBER}]")
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up and finalizing...'
            slackSend (color: '#FF0000', message: "Job finished: ${env.JOB_NAME} [${env.BUILD_NUMBER}]")
        }
        success {
            slackSend (color: 'good', message: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' completed successfully.")
        }
        failure {
            slackSend (color: 'danger', message: "FAILURE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' failed.")
        }
    }
}

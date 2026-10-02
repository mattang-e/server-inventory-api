pipeline {
    agent any

    stages {
        stage('Checkout Test') {
            steps {
                sh 'echo "Git checkout successful"'
                sh 'whoami'
                sh 'pwd'
                sh 'ls -al'
            }
        }
        stage('Build Image') {
            steps {
                sh 'echo "XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR"'
                sh 'podman build -t server-inventory-api:test .'
            }
        }
    }
}
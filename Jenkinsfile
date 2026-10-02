pipeline {
    agent any

    environment {
        HARBOR_REGISTRY = 'harbor.lab.local'
        HARBOR_PROJECT = 'server-inventory'
        IMAGE_NAME = 'server-inventory-api'
    }

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
                sh '''
                    podman build \
                        -t ${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'harbor-credentials',
                        usernameVariable: 'HARBOR_USER',
                        passwordVariable: 'HARBOR_PASSWORD'
                    )
                ]) {
                    sh '''
                        printf '%s' "$HARBOR_PASSWORD" | \
                          podman login ${HARBOR_REGISTRY} \
                          --username "$HARBOR_USER" \
                          --password-stdin

                          podman push \
                            ${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${IMAGE_NAME}:${BUILD_NUMBER}
                    '''
                }
            }
        }
    }
}
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

class Agent:
    def __init__(self, state_size, action_size, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = device
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)  # Replay memory buffer
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.epsilon_decay = 0.995  # Exploration decay rate
        self.learning_rate = 0.001  # Learning rate
        
        # Define the neural network model
        self.model = self._build_model()
        
        # Move model to GPU if available
        self.model.to(self.device)
        
        # Define optimizer
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        # Define loss function
        self.criterion = nn.MSELoss()
        
        self.filename = 'agentmodel.pth'
        print(self.model)

    def _build_model(self):
        model = nn.Sequential(
            nn.Linear(self.state_size, 24),
            nn.ReLU(),
            nn.Linear(24, 24),
            nn.ReLU(),
            nn.Linear(24, self.action_size)
        )
        return model

    def remember(self, state, action, reward, next_state, done):
        print(f"Storing memory: state shape {state.shape}, action {action}, reward {reward}")
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # Convert state to tensor and move to device
        state = torch.FloatTensor(state).to(self.device)
        
        # Epsilon-greedy action selection
        # if np.random.rand() <= self.epsilon:
        #     return np.random.choice(self.action_size)
        
        # Predict action values
        with torch.no_grad():
            act_values = self.model(state)
        
        # Return the action with the highest predicted value
        return torch.argmax(act_values).item()

    def replay(self, batch_size):
    # Check if we have enough samples in memory
        # if len(self.memory) < batch_size:
        #     return
        
        # Sample a minibatch from memory
        minibatch = random.sample(self.memory, batch_size)
        
        # Prepare batch tensors
        states = torch.FloatTensor(np.array([s[0] for s in minibatch])).to(self.device)
        actions = torch.LongTensor([s[1] for s in minibatch]).to(self.device)
        rewards = torch.FloatTensor([s[2] for s in minibatch]).to(self.device)
        next_states = torch.FloatTensor(np.array([s[3] for s in minibatch])).to(self.device)
        dones = torch.FloatTensor([s[4] for s in minibatch]).to(self.device)
        
        # Ensure states are 2D tensor [batch_size, state_size]
        states = states.view(batch_size, -1)
        next_states = next_states.view(batch_size, -1)
        
        # Compute current Q values
        current_q_values = self.model(states).gather(1, actions.unsqueeze(1))
        
        # Compute target Q values
        with torch.no_grad():
            max_next_q_values = self.model(next_states).max(1)[0]
            target_q_values = rewards + (self.gamma * max_next_q_values * (1 - dones))
        
        # Compute loss
        loss = nn.functional.mse_loss(current_q_values.squeeze(), target_q_values)
        
        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, filename=None):
        # Use default filename if not provided
        if filename is None:
            filename = self.filename
        torch.save(self.model.state_dict(), filename)

    def load(self, filename=None):
        # Use default filename if not provided
        if filename is None:
            filename = self.filename
        self.model.load_state_dict(torch.load(filename))
        self.model.eval()  # Set the model to evaluation mode
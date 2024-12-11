import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os

class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super(PolicyNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Softmax(dim=-1)
        )
    
    def forward(self, state):
        return self.network(state)

class PolicyGradientAgent:
    def __init__(self, state_dim, action_dim, learning_rate=1e-3, gamma=0.99):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policy_network = PolicyNetwork(state_dim, action_dim).to(self.device)
        self.optimizer = optim.Adam(self.policy_network.parameters(), lr=learning_rate)
        self.gamma = gamma
        
        # Storage for episode data
        self.saved_log_probs = []
        self.rewards = []
        
    def select_action(self, state):
        """Select an action from the policy network"""
        # Convert state to tensor if it's not already
        if isinstance(state, np.ndarray):
            state = torch.FloatTensor(state).to(self.device)
        
        # Ensure state has batch dimension
        if state.dim() == 1:
            state = state.unsqueeze(0)
            
        # Get action probabilities
        action_probs = self.policy_network(state)
        
        # Sample action from the probability distribution
        action_distribution = torch.distributions.Categorical(action_probs)
        action = action_distribution.sample()
        
        # Store log probability for training
        self.saved_log_probs.append(action_distribution.log_prob(action))
        
        return action.item()

    def store_reward(self, reward):
        """Store a reward for the current timestep"""
        self.rewards.append(reward)

    def update_policy(self):
        """Update the policy network using the collected episode data"""
        if len(self.rewards) == 0:
            return
            
        # Calculate discounted rewards
        returns = []
        R = 0
        for r in reversed(self.rewards):
            R = r + self.gamma * R
            returns.insert(0, R)
            
        # Convert returns to tensor and normalize
        returns = torch.tensor(returns, dtype=torch.float32).to(self.device)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        # Calculate policy loss
        policy_loss = []
        for log_prob, R in zip(self.saved_log_probs, returns):
            policy_loss.append(-log_prob * R)  # Negative because we're doing gradient ascent
            
        # Sum up all the losses
        policy_loss = torch.cat(policy_loss).sum()
        
        # Perform backpropagation
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()
        
        # Clear episode data
        self.saved_log_probs.clear()
        self.rewards.clear()

    def save(self, filepath):
        """Save the model"""
        save_dict = {
            'model_state_dict': self.policy_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'gamma': self.gamma
        }
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        torch.save(save_dict, filepath)
        
    def load(self, filepath):
        """Load the model"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No model found at {filepath}")
        
        checkpoint = torch.load(filepath, map_location=self.device)
        self.policy_network.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.gamma = checkpoint['gamma']
# React 19 Patterns Guide for LLMs

## CORRECT Patterns

### 1. Custom Hooks
```javascript
// DO: Extract reusable logic
function useUserData(userId) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchUser(userId).then(data => {
      setUser(data);
      setLoading(false);
    });
  }, [userId]);
  
  return { user, loading };
}

// Usage
function UserProfile({ userId }) {
  const { user, loading } = useUserData(userId);
  if (loading) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

### 2. Compound Components
```javascript
// DO: Components that work together
function Card({ children }) {
  return <div className="card">{children}</div>;
}

Card.Header = function CardHeader({ children }) {
  return <div className="card-header">{children}</div>;
};

Card.Body = function CardBody({ children }) {
  return <div className="card-body">{children}</div>;
};

// Usage
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>
```

### 3. Container/Presentational Split
```javascript
// DO: Separate logic from presentation
function UserListContainer() {
  const { users, loading } = useUsers();
  return <UserList users={users} loading={loading} />;
}

function UserList({ users, loading }) {
  if (loading) return <div>Loading...</div>;
  return (
    <ul>
      {users.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}
```

### 4. React 19 Form Actions
```javascript
// DO: Use async form actions
function UserForm({ user }) {
  async function updateUser(formData) {
    const name = formData.get('name');
    await api.updateUser(user.id, { name });
  }
  
  return (
    <form action={updateUser}>
      <input name="name" defaultValue={user.name} />
      <button type="submit">Update</button>
    </form>
  );
}
```

### 5. useOptimistic Hook
```javascript
// DO: Optimistic updates
function TodoList({ todos }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo) => [...state, { ...newTodo, pending: true }]
  );
  
  async function addTodo(text) {
    addOptimisticTodo({ id: Date.now(), text });
    await api.createTodo(text);
  }
  
  return (
    <div>
      {optimisticTodos.map(todo => (
        <div key={todo.id} className={todo.pending ? 'pending' : ''}>
          {todo.text}
        </div>
      ))}
    </div>
  );
}
```

### 6. Error Boundaries
```javascript
// DO: Catch errors properly
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

### 7. React 19 Direct Refs
```javascript
// DO: Use refs directly (no forwardRef needed)
function Button({ ref, children, onClick }) {
  return (
    <button ref={ref} onClick={onClick}>
      {children}
    </button>
  );
}
```

### 8. Proper useEffect Dependencies
```javascript
// DO: Include all dependencies
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]); // ✅ userId in dependencies
  
  return <div>{user?.name}</div>;
}
```

## INCORRECT Antipatterns

### 1. Array Index as Keys
```javascript
// DON'T: Use array index as key
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map((todo, index) => (
        <li key={index}>{todo.text}</li> // ❌ Index as key
      ))}
    </ul>
  );
}

// DO: Use stable unique IDs
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.text}</li> // ✅ Stable ID
      ))}
    </ul>
  );
}
```

### 2. Direct State Mutation
```javascript
// DON'T: Mutate state directly
function TodoList({ todos, setTodos }) {
  function addTodo(text) {
    todos.push({ id: Date.now(), text }); // ❌ Direct mutation
    setTodos(todos);
  }
}

// DO: Create new arrays/objects
function TodoList({ todos, setTodos }) {
  function addTodo(text) {
    setTodos(prev => [...prev, { id: Date.now(), text }]); // ✅ New array
  }
}
```

### 3. Components Inside Components
```javascript
// DON'T: Define components inside components
function Parent({ items }) {
  function Child({ item }) { // ❌ Re-created every render
    return <div>{item.name}</div>;
  }
  
  return (
    <div>
      {items.map(item => <Child key={item.id} item={item} />)}
    </div>
  );
}

// DO: Define components outside
function Child({ item }) { // ✅ Stable component
  return <div>{item.name}</div>;
}

function Parent({ items }) {
  return (
    <div>
      {items.map(item => <Child key={item.id} item={item} />)}
    </div>
  );
}
```

### 4. Missing useEffect Dependencies
```javascript
// DON'T: Omit dependencies
function UserProfile({ userId, onUserLoad }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(user => {
      setUser(user);
      onUserLoad(user);
    });
  }, []); // ❌ Missing userId, onUserLoad
}

// DO: Include all dependencies
function UserProfile({ userId, onUserLoad }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(user => {
      setUser(user);
      onUserLoad(user);
    });
  }, [userId, onUserLoad]); // ✅ All dependencies included
}
```

### 5. Inline Functions in JSX
```javascript
// DON'T: Create functions in render
function TodoList({ todos, onDelete }) {
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          {todo.text}
          <button onClick={() => onDelete(todo.id)}> // ❌ New function each render
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}

// DO: Use useCallback for stable references
function TodoList({ todos, onDelete }) {
  const handleDelete = useCallback((id) => {
    onDelete(id);
  }, [onDelete]);
  
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          {todo.text}
          <button onClick={() => handleDelete(todo.id)}> // ✅ Stable reference
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}
```

### 6. Massive Components
```javascript
// DON'T: 500+ line components with everything mixed
function UserDashboard() {
  // ❌ Hundreds of lines of mixed concerns
  const [users, setUsers] = useState([]);
  const [posts, setPosts] = useState([]);
  const [comments, setComments] = useState([]);
  // ... 400+ more lines
  
  return (
    <div>
      {/* Massive JSX with everything */}
    </div>
  );
}

// DO: Break into focused components
function UserDashboard() {
  return (
    <div>
      <UserList />
      <PostList />
      <CommentList />
    </div>
  );
}
```

### 7. No Prop Validation
```javascript
// DON'T: Accept any props
function Button(props) { // ❌ No validation
  return <button {...props} />;
}

// DO: Use TypeScript or PropTypes
interface ButtonProps {
  onClick: () => void;
  disabled?: boolean;
  children: React.ReactNode;
}

function Button({ onClick, disabled = false, children }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}
```

### 8. Excessive Prop Drilling
```javascript
// DON'T: Pass props through many levels
function App() {
  const user = useUser();
  return <Layout user={user} />;
}

function Layout({ user }) {
  return <Sidebar user={user} />; // ❌ Passing through
}

function Sidebar({ user }) {
  return <UserMenu user={user} />; // ❌ Passing through
}

// DO: Use Context for deeply nested data
const UserContext = createContext();

function App() {
  const user = useUser();
  return (
    <UserContext.Provider value={user}>
      <Layout />
    </UserContext.Provider>
  );
}

function UserMenu() {
  const user = useContext(UserContext); // ✅ Direct access
  return <div>{user.name}</div>;
}
```

## Common Linting Violations (ESLint/TypeScript)

### TypeScript Any Usage
```typescript
// DON'T: Use any type
function processData(data: any): any {  // ❌ any types
  return data.whatever.something;
}

const user: any = await fetchUser();  // ❌ any type

// DO: Proper typing
interface User {
  id: number;
  name: string;
}

function processData(data: User): string {  // ✅ Proper types
  return data.name;
}

const user: User = await fetchUser();  // ✅ Typed response
```

### Nullish Coalescing & Optional Chaining
```typescript
// DON'T: Unsafe property access
function getUserName(user: User | null) {
  return user.name || 'Anonymous';  // ❌ Runtime error if user is null
}

const email = user.profile.email;  // ❌ Unsafe nesting

// DO: Safe property access
function getUserName(user: User | null) {
  return user?.name ?? 'Anonymous';  // ✅ Safe access
}

const email = user?.profile?.email ?? '';  // ✅ Safe chaining
```

### Unused Variables/Imports
```typescript
// DON'T: Unused imports/variables
import React, { useState, useEffect } from 'react';  // ❌ useEffect unused
import { debounce } from 'lodash';  // ❌ debounce unused

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);  // ❌ loading unused
  const tempVar = 'hello';  // ❌ unused variable
  
  return <div>{user?.name}</div>;
}

// DO: Only import/declare what you use
import React, { useState } from 'react';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  
  return <div>{user?.name}</div>;
}
```

### Missing Return Types
```typescript
// DON'T: No return type annotations
function calculateTotal(items: Item[]) {  // ❌ No return type
  return items.reduce((sum, item) => sum + item.price, 0);
}

async function fetchUser(id: string) {  // ❌ No return type
  return await api.get(`/users/${id}`);
}

// DO: Explicit return types
function calculateTotal(items: Item[]): number {  // ✅ Return type
  return items.reduce((sum, item) => sum + item.price, 0);
}

async function fetchUser(id: string): Promise<User> {  // ✅ Return type
  return await api.get(`/users/${id}`);
}
```

### Event Handler Types
```typescript
// DON'T: Any or missing event types
function handleClick(event: any) {  // ❌ any type
  event.preventDefault();
}

function handleSubmit(event) {  // ❌ No type
  event.preventDefault();
}

// DO: Proper event types
function handleClick(event: React.MouseEvent<HTMLButtonElement>) {
  event.preventDefault();
}

function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault();
}
```

### Array/Object Destructuring
```typescript
// DON'T: Unsafe destructuring
const user = getUser();
const name = user.name;  // ❌ Could be undefined
const { email } = user.profile;  // ❌ profile could be undefined

// DO: Safe destructuring
const user = getUser();
const name = user?.name ?? 'Unknown';
const { email } = user?.profile ?? {};
```

### Console Statements
```typescript
// DON'T: Console statements in production code
function processData(data: any[]) {
  console.log('Processing data:', data);  // ❌ Console statement
  console.error('Debug info');  // ❌ Console statement
  return data.map(item => item.id);
}

// DO: Remove console statements (use proper logging)
function processData(data: Item[]): number[] {
  // Use proper logging library instead
  return data.map(item => item.id);
}
```

### Comparison Operators
```typescript
// DON'T: Loose equality
if (user.id == '123') {  // ❌ Loose equality
  // code
}

if (user.active != false) {  // ❌ Loose inequality
  // code
}

// DO: Strict equality
if (user.id === '123') {  // ✅ Strict equality
  // code
}

if (user.active !== false) {  // ✅ Strict inequality
  // code
}
```

### Async/Await vs Promises
```typescript
// DON'T: Missing await or mixed patterns
async function fetchUserData() {
  const user = fetchUser();  // ❌ Missing await
  return user.then(u => u.name);  // ❌ Mixing async/await with .then()
}

// DO: Consistent async/await
async function fetchUserData(): Promise<string> {
  const user = await fetchUser();  // ✅ Proper await
  return user.name;
}
```

### Interface vs Type
```typescript
// DON'T: Inconsistent usage
type User = {  // ❌ Use interface for object shapes
  id: number;
  name: string;
};

interface ApiResponse = string | number;  // ❌ Use type for unions

// DO: Proper usage
interface User {  // ✅ Interface for object shapes
  id: number;
  name: string;
}

type ApiResponse = string | number;  // ✅ Type for unions
```

### Hook Dependencies
```typescript
// DON'T: Missing or incorrect dependencies
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, []);  // ❌ Missing userId dependency
  
  const handleUpdate = useCallback(() => {
    updateUser(userId, user);
  }, [user]);  // ❌ Missing userId dependency
}

// DO: Correct dependencies
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);  // ✅ Include userId
  
  const handleUpdate = useCallback(() => {
    updateUser(userId, user);
  }, [userId, user]);  // ✅ Include all dependencies
}
```

## Component Size Limits
- ✅ Max 200 lines per component
- ✅ Max 10 props per component
- ✅ Single responsibility principle
- ✅ Break into smaller components when exceeding limits

## React 19 New Features to Use
- ✅ `use()` API for reading resources
- ✅ `useFormStatus()` for form state
- ✅ `useActionState()` for async actions
- ✅ Document metadata management
- ✅ Direct ref prop access (no forwardRef)

## TypeScript Requirements
```typescript
// DO: Always type props and state
interface Props {
  user: User;
  onUpdate: (user: User) => void;
}

function UserProfile({ user, onUpdate }: Props) {
  const [isEditing, setIsEditing] = useState<boolean>(false);
  // Component implementation
}
```
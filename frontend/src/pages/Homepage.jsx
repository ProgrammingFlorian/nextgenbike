import { Home } from "../assets/svgs";

export default function Homepage() {
  return (
    <div className="p-9 mt-4">
      {/* Welcome Message */}
      <div className="flex flex-col gap-0.5">
        <h1 className="text-2xl font-bold">Welcome back!</h1>
        <p className="text-gray">Ready to pedal into adventure?</p>
      </div>

      {/* Activities Section */}
      <div className="mt-6">
        <h2 className="text-lg font-semibold">Your Activities</h2>
        <div className="p-3 border border-gray rounded-xl mt-4">
          <div className="grid grid-cols-6 items-center p-2">
            <Home fill="green" />
            <span className="col-span-2 font-bold text-lg my-auto">76km</span>
            <span className="col-span-3 my-auto">Cycled this week</span>
          </div>
          <div className="p-3 border border-gray rounded-md mt-2 border-opacity-80 flex flex-col gap-1.5">
            <div className="grid grid-cols-6 items-center p-1">
              <Home fill="green" />
              <span className="col-span-2 font-bold text-lg my-auto">76km</span>
              <span className="col-span-3 my-auto">Cycled this week</span>
            </div>
            <hr className="text-gray opacity-80" />
            <div className="grid grid-cols-6 items-center p-1">
              <Home fill="green" />
              <span className="col-span-2 font-bold text-lg my-auto">76km</span>
              <span className="col-span-3 my-auto">Cycled this week</span>
            </div>
            <hr className="text-gray opacity-80" />
            <div className="grid grid-cols-6 items-center p-1">
              <Home fill="green" />
              <span className="col-span-2 font-bold text-lg my-auto">76km</span>
              <span className="col-span-3 my-auto">Cycled this week</span>
            </div>
          </div>
        </div>
      </div>

      {/* Latest Trip Section */}
      <div className="mt-6">
        <h2 className="text-lg font-semibold">Your Latest Trip</h2>
      </div>
    </div>
  );
}

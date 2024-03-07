import { expect } from "chai";
import { createPushNotificationsJobs } from "./8-job";
import { createQueue } from "kue";

describe("createPushNotificationsJobs", () => {
  let queue;
  before(() => {
    queue = createQueue();
    queue.testMode.enter();
  });
  before(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });
  it("should display an error message if jobs is not an array", () => {
    expect(() => createPushNotificationsJobs("jobs", queue)).to.throw(
      "Jobs is not an array"
    );
  });
  it("should create two jobs", () => {
    const jobs = [
      {
        phoneNumber: "4153518780",
        message: "This is the code 1234 to verify your account",
      },
      {
        phoneNumber: "4153518781",
        message: "This is the code 4562 to verify your account",
      },
    ];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal("push_notification_code_3");
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[1].type).to.equal("push_notification_code_3");
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
  });
});

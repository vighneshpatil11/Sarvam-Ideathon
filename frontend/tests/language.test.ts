import { describe,expect,it } from "vitest"; import { messages } from "../src/i18n";
describe("language dictionaries",()=>{it("provide core labels in all supported languages",()=>{for(const language of ["en","hi","mr"] as const){expect(messages[language].home).toBeTruthy();expect(messages[language].disclaimer).toBeTruthy();expect(messages[language].searchPlaceholder).toBeTruthy();}});});

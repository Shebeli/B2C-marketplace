"use server";

import { revalidatePath } from "next/cache";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export async function signOut(path: string) {
  try {
    const cookieStore = await cookies();
    cookieStore.delete("access_token");
    cookieStore.delete("refresh_token");
  } catch (error) {
    console.error("Failed to logout the user with server action:", error);
    throw new Error("Failed to logout the user.");
  }

  revalidatePath(path);
  redirect(path);
}
